import pytest
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import ChangePassword, CreatePasswordUser
from server.application.auth.queries import LoginPasswordUser
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.domain.auth.exceptions import LoginFailed
from server.seedwork.application.messages import MessageBus


@pytest.mark.asyncio
async def test_changepassword(temp_org: OrganizationView) -> None:
    bus = resolve(MessageBus)
    email = EmailStr("changepassworduser@mydomain.org")

    await bus.execute(
        CreatePasswordUser(
            organization_siret=temp_org.siret,
            email=email,
            password=SecretStr("initialpwd"),
        )
    )

    await bus.execute(ChangePassword(email=email, password=SecretStr("newpwd")))

    with pytest.raises(LoginFailed):
        await bus.execute(
            LoginPasswordUser(email=email, password=SecretStr("initialpwd"))
        )

    await bus.execute(LoginPasswordUser(email=email, password=SecretStr("newpwd")))
