import asyncio
import sys

import click
from pydantic import EmailStr, SecretStr
from typing import List

from server.application.auth.commands import ChangePassword
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import PasswordUser
from server.domain.auth.repositories import PasswordUserRepository
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus


async def main() -> None:
    bus = resolve(MessageBus)
    tag_repository = resolve(TagRepository)

    tags = tag_repository.get_all()

    tags_duplicate : dict[str, List[str, str]] = {}

    for tag in tags:
        if tags_duplicate[tag.name] is not None:
            tags_duplicate[tag.name].append(tag.id)
            



    await bus.execute(
        ChangePassword(email=EmailStr(user.account.email), password=password)
    )


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
