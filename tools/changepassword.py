import asyncio
import sys

import click
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import ChangePassword
from server.config.di import bootstrap, resolve
from server.domain.auth.entities import PasswordUser
from server.domain.auth.repositories import PasswordUserRepository
from server.seedwork.application.messages import MessageBus


async def _prompt_password_user() -> PasswordUser:
    repository = resolve(PasswordUserRepository)

    email = click.prompt("Email")

    password_user = await repository.get_by_email(email)

    if password_user is None:
        click.echo(click.style(f"PasswordUser does not exist: {email}", fg="red"))
        sys.exit(1)

    return password_user


def _prompt_password() -> SecretStr:
    return click.prompt(
        "Password",
        confirmation_prompt="Password (repeat)",
        value_proc=SecretStr,
        hide_input=True,
    )


async def main() -> None:
    bus = resolve(MessageBus)

    user = await _prompt_password_user()
    password = _prompt_password()

    await bus.execute(
        ChangePassword(email=EmailStr(user.account.email), password=password)
    )


if __name__ == "__main__":
    bootstrap()
    asyncio.run(main())
