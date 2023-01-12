import json
import re
import uuid
from pathlib import Path

import pytest
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import DeletePasswordUser
from server.application.auth.queries import LoginPasswordUser
from server.application.datasets.commands import UpdateDataset
from server.application.datasets.queries import GetAllDatasets, GetDatasetByID
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.domain.common.types import ID, Skip
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
        organizations: []
        catalogs: []
        formats: []

        """
    )
    code = await initdata.main(path)
    assert code == 0

    pagination = await bus.execute(GetAllDatasets(account=Skip()))
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
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    temp_org: OrganizationView,
    value: str,
) -> None:
    path = tmp_path / "initdata.yml"
    path.write_text(
        """
        organizations: []
        catalogs: []
        users:
          - id: 9c2cefce-ea47-4e6e-8c79-8befd4495f45
            params:
              organization_siret: "{siret}"
              email: test@admin.org
              password: __env__
        tags: []
        datasets: []
        formats: []
        """.format(
            siret=temp_org.siret
        )
    )

    monkeypatch.setenv("TOOLS_PASSWORDS", value)

    with pytest.raises(ValueError):
        await initdata.main(path, no_input=True)


@pytest.mark.asyncio
async def test_initdata_env_password(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, temp_org: OrganizationView
) -> None:
    bus = resolve(MessageBus)

    path = tmp_path / "initdata.yml"
    path.write_text(
        """
        organizations: []
        catalogs: []
        users:
          - id: 9c2cefce-ea47-4e6e-8c79-8befd4495f45
            params:
              organization_siret: "{siret}"
              email: test@admin.org
              password: __env__
        tags: []
        datasets: []
        formats: []

        """.format(
            siret=temp_org.siret
        )
    )

    # Env variable is used to create the user.
    monkeypatch.setenv("TOOLS_PASSWORDS", json.dumps({"test@admin.org": "testpwd"}))
    code = await initdata.main(path, no_input=True)
    assert code == 0

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
    env_example = Path(".env.example").read_text()
    m = re.search("TOOLS_PASSWORDS='(.*)'", env_example)
    assert m is not None
    monkeypatch.setenv("TOOLS_PASSWORDS", m.group(1))

    num_users = 4
    num_tags = 9
    num_datasets = 5
    num_organizations = 2
    num_catalogs = 1
    num_formats = 3
    num_entities = (
        num_users
        + num_tags
        + num_datasets
        + num_catalogs
        + num_organizations
        + num_formats
    )

    code = await initdata.main(path, no_input=True)
    assert code == 0
    captured = capsys.readouterr()

    print(captured.out)
    assert captured.out.count("created") == num_entities

    pk = ID(uuid.UUID("16b398af-f8c7-48b9-898a-18ad3404f528"))
    dataset = await bus.execute(GetDatasetByID(id=pk, account=Skip()))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Run a second time, without changes.
    code = await initdata.main(path)
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities

    # Make a change.
    command = UpdateDataset(
        account=Skip(),
        **dataset.dict(exclude={"title"}),
        format_ids=[format.id for format in dataset.formats],
        tag_ids=[tag.id for tag in dataset.tags],
        title="Changed",
    )
    await bus.execute(command)
    dataset = await bus.execute(GetDatasetByID(id=pk, account=Skip()))
    assert dataset.title == "Changed"

    # No reset: dataset left unchanged
    code = await initdata.main(path)
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities
    dataset = await bus.execute(GetDatasetByID(id=pk, account=Skip()))
    assert dataset.title == "Changed"

    # Reset: dataset goes back to initial state defined in yml file
    code = await initdata.main(path, reset=True)
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities - 1
    assert captured.out.count("reset") == 1
    dataset = await bus.execute(GetDatasetByID(id=pk, account=Skip()))
    assert dataset.title == "Données brutes de l'inventaire forestier"

    # Reset: dataset left in initial state
    code = await initdata.main(path, reset=True)
    assert code == 0
    captured = capsys.readouterr()
    assert captured.out.count("ok") == num_entities
    dataset = await bus.execute(GetDatasetByID(id=pk, account=Skip()))
    assert dataset.title == "Données brutes de l'inventaire forestier"


@pytest.mark.asyncio
async def test_environment_initdata_files_are_valid(ops_environments_dir: Path) -> None:
    initdata_paths = [
        initdata_path
        for env_dir in ops_environments_dir.iterdir()
        if (initdata_path := env_dir / "assets" / "initdata.yml").exists()
    ]

    assert (
        initdata_paths
    ), "No environment initdata.yml found: has their location changed?"

    for initdata_path in initdata_paths:
        code = await initdata.main(initdata_path, check=True)
        assert code == 0, initdata_path
