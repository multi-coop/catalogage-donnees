import argparse
import asyncio
import functools
import json
import os
import pathlib
from typing import Any, Dict

import click
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, parse_raw_as

from server.application.auth.commands import CreatePasswordUser
from server.application.datasets.commands import CreateDataset, UpdateDataset
from server.application.tags.commands import CreateTag
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import UserRole
from server.domain.auth.repositories import PasswordUserRepository
from server.domain.datasets.entities import Dataset
from server.domain.datasets.repositories import DatasetRepository
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus

load_dotenv()

info = functools.partial(click.style, fg="blue")
success = functools.partial(click.style, fg="bright_green")
warn = functools.partial(click.style, fg="yellow")
error = functools.partial(click.style, fg="red")


def ruler(text: str) -> str:
    return click.style(f"──── {text}", fg="magenta")


class UserExtras(BaseModel):
    role: UserRole = UserRole.USER


def _parse_env_passwords(passwords_env: str) -> Dict[str, str]:
    try:
        return parse_raw_as(Dict[str, str], passwords_env or "{}")
    except json.JSONDecodeError:
        raise ValueError("Malformed TOOLS_PASSWORDS: invalid JSON")
    except ValidationError as exc:
        raise ValueError(f"Malformed TOOLS_PASSWORDS: {exc}")


async def handle_user(
    item: dict, *, no_input: bool, env_passwords: Dict[str, str]
) -> None:
    bus = resolve(MessageBus)
    repository = resolve(PasswordUserRepository)

    email = item["params"]["email"]
    existing_user = await repository.get_by_email(email)

    if existing_user is not None:
        print(f"{info('ok')}: PasswordUser(email={email!r}, ...)")
        return

    extras = UserExtras(**item.get("extras", {}))

    if item["params"]["password"] == "__env__":
        password = env_passwords.get(email)
        if password is None:
            if no_input:
                raise RuntimeError(
                    f"would prompt password for {email!r}, "
                    "please include '<email>=<password>' in TOOLS_PASSWORDS "
                    "environment variable"
                )
            password = click.prompt(f"Password for {email}", hide_input=True)
        item["params"]["password"] = password

    command = CreatePasswordUser(**item["params"])
    await bus.execute(command, id_=item["id"], **extras.dict())
    print(f"{success('created')}: {command!r}")


async def handle_tag(item: dict) -> None:
    bus = resolve(MessageBus)
    repository = resolve(TagRepository)

    id_ = item["id"]
    existing_tag = await repository.get_by_id(id_)

    if existing_tag is not None:
        print(f"{info('ok')}: {existing_tag!r}")
        return

    command = CreateTag(**item["params"])
    await bus.execute(command, id_=item["id"])
    print(f"{success('created')}: {command!r}")


async def handle_dataset(item: dict, reset: bool = False) -> None:
    def _get_dataset_attr(dataset: Dataset, attr: str) -> Any:
        if attr == "tag_ids":
            return [tag.id for tag in dataset.tags]
        return getattr(dataset, attr)

    bus = resolve(MessageBus)
    repository = resolve(DatasetRepository)

    id_ = item["id"]
    existing_dataset = await repository.get_by_id(id_)

    if existing_dataset is not None:
        update_command = UpdateDataset(id=id_, **item["params"])

        changed = any(
            getattr(update_command, k) != _get_dataset_attr(existing_dataset, k)
            for k in item["params"]
        )

        if changed and reset:
            await bus.execute(update_command)
            print(f"{warn('reset')}: {update_command!r}")
            return

        dataset_repr = f"Dataset(id={id_!r}, title={item['params']['title']!r}, ...)"
        print(f"{info('ok')}: {dataset_repr}")
        return

    create_command = CreateDataset(**item["params"])

    await bus.execute(create_command, id_=id_)
    print(f"{success('created')}: {create_command!r}")


async def main(path: pathlib.Path, reset: bool = False, no_input: bool = False) -> None:
    with path.open() as f:
        spec = yaml.safe_load(f)

    print("\n", ruler("Users"))

    env_passwords = _parse_env_passwords(os.getenv("TOOLS_PASSWORDS", ""))

    for item in spec["users"]:
        await handle_user(item, no_input=no_input, env_passwords=env_passwords)

    print("\n", ruler("Tags"))

    for item in spec["tags"]:
        await handle_tag(item)

    print("\n", ruler("Datasets"))

    for item in spec["datasets"]:
        await handle_dataset(item, reset=reset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=pathlib.Path)
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--no-input", action="store_true")
    args = parser.parse_args()

    bootstrap()

    asyncio.run(main(path=args.path, reset=args.reset, no_input=args.no_input))
