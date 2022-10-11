import pytest
from pydantic import EmailStr, SecretStr

from server.application.auth.commands import ChangePassword, CreatePasswordUser
from server.application.auth.queries import LoginPasswordUser
from server.application.organizations.views import OrganizationView
from server.config.di import resolve
from server.domain.auth.exceptions import LoginFailed
from server.domain.auth.repositories import AccountRepository, PasswordUserRepository
from server.seedwork.application.messages import MessageBus
from tests.factories import (
    CreateDataPassUserFactory,
    CreateOrganizationFactory,
    CreatePasswordUserFactory,
)


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


@pytest.mark.asyncio
class TestCreatePasswordUser:
    async def test_existing_datapass_user_reuses_account(self) -> None:
        bus = resolve(MessageBus)

        email = "johndoe@mydomain.org"
        siret = "11122233344441"

        await bus.execute(CreateOrganizationFactory.build(siret=siret))
        await bus.execute(
            CreateDataPassUserFactory.build(organization_siret=siret, email=email)
        )
        account_repository = resolve(AccountRepository)
        existing_account = await account_repository.get_by_email(email)

        await bus.execute(
            CreatePasswordUserFactory.build(organization_siret=siret, email=email)
        )
        repository = resolve(PasswordUserRepository)
        user = await repository.get_by_email(email)
        assert user is not None
        assert user.account == existing_account

    async def test_existing_datapass_user_in_different_org_is_error(self) -> None:
        bus = resolve(MessageBus)

        email = "johndoe@mydomain.org"
        siret_1 = "11122233344441"
        siret_2 = "11122233344442"

        await bus.execute(CreateOrganizationFactory.build(siret=siret_1))
        await bus.execute(CreateOrganizationFactory.build(siret=siret_2))
        await bus.execute(
            CreateDataPassUserFactory.build(organization_siret=siret_1, email=email)
        )

        with pytest.raises(
            RuntimeError,
            match="requested to create a PasswordUser in different organization",
        ):
            await bus.execute(
                CreatePasswordUserFactory.build(organization_siret=siret_2, email=email)
            )
