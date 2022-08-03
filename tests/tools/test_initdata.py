import json
import uuid
from pathlib import Path

import pytest
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import DeletePasswordUser
from server.application.auth.queries import LoginPasswordUser
from server.application.datasets.commands import UpdateDataset
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.config.di import resolve
from server.domain.common.types import ID
from server.seedwork.application.messages import MessageBus
from tools import initdata


@pytest.mark.asyncio
async def test_initdata_empty(tmp_path: Path) -> None:
    bus = resolve(MessageBus)

    path = tmp_path / "initdata.yml"
    path.write_text(
        """
        users: []
        tags: []
        datasets: []
        """
    )
    await initdata.main(path)

    pagination = await bus.execute(GetAllDatasets())
    assert pagination.items == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        pytest.param('{"missingquote: "pwd"}', id="invalid-json"),
        pytest.param('["email", "pwd"]', id="not-dict"),
    ],
)
async def test_initdata_env_password_invalid(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, value: str
) -> None:
    path = tmp_path / "initdata.yml"
    path.write_text(
        """
        users:
          - id: 9c2cefce-ea47-4e6e-8c79-8befd4495f45
            params:
              email: test@admin.org
              password: __env__
        datasets: []
        """
    )

    monkeypatch.setenv("TOOLS_PASSWORDS", value)

    with pytest.raises(ValueError):
        await initdata.main(path, no_input=True)


@pytest.mark.asyncio
async def test_initdata_env_password(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    bus = resolve(MessageBus)

    path = tmp_path / "initdata.yml"
    path.write_text(
        """
        users:
          - id: 9c2cefce-ea47-4e6e-8c79-8befd4495f45
            params:
              email: test@admin.org
              password: __env__
        tags: []
        datasets: []
        """
    )

    # Env variable is used to create the user.
    monkeypatch.setenv("TOOLS_PASSWORDS", json.dumps({"test@admin.org": "testpwd"}))
    await initdata.main(path, no_input=True)

    account = await bus.execute(
        LoginPasswordUser(
            email=EmailStr("test@admin.org"), password=SecretStr("testpwd")
        )
    )

    # (Delete user to prevent email collision below.)
    await bus.execute(DeletePasswordUser(account_id=account.id))

    # If not set, it would be prompted in the terminal.
    monkeypatch.delenv("TOOLS_PASSWORDS")
    with pytest.raises(RuntimeError) as ctx:
        await initdata.main(path, no_input=True)
    assert "would prompt" in str(ctx.value)
    assert "TOOLS_PASSWORDS" in str(ctx.value)


@pytest.mark.asyncio
async def test_repo_initdata(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    bus = resolve(MessageBus)
    path = Path("tools", "initdata.yml")
    monkeypatch.setenv(
        "TOOLS_PASSWORDS", json.dumps({"admin@catalogue.data.gouv.fr": "test"})
    )

    num_users = 2
    num_tags = 7
    num_datasets = 4
    num_entities = num_users + num_tags + num_datasets

    await initdata.main(path, no_input=True)
    captured = capsys.readouterr()
    assert captured.out.count("created") == num_entities

    pk = ID(uuid.UUID("16b398af-f8c7-48b9-898a-18ad3404f528"))
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Run a second time, without changes.
    await initdata.main(path)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities

    # Make a change.
    command = UpdateDataset(
        **dataset.dict(exclude={"title"}),
        tag_ids=[tag.id for tag in dataset.tags],
        title="Changed",
    )
    await bus.execute(command)
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Changed"

    # No reset: dataset left unchanged
    await initdata.main(path)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Changed"

    # Reset: dataset goes back to initial state defined in yml file
    await initdata.main(path, reset=True)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities - 1
    assert captured.out.count("reset") == 1
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Reset: dataset left in initial state
    await initdata.main(path, reset=True)
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities
    dataset = await bus.execute(GetDatasetByID(id=pk))
    assert dataset.title == "Données brutes de l'inventaire forestier"
