from typing import Optional

from server.application.auth.views import AccountView, AuthenticatedAccountView
from server.application.organizations.queries import GetOrganizationBySiret
from server.config.di import resolve
from server.domain.auth.entities import Account, DataPassUser, PasswordUser, UserRole
from server.domain.auth.exceptions import (
    AccountDoesNotExist,
    DataPassUserAlreadyExists,
    EmailAlreadyExists,
    LoginFailed,
)
from server.domain.auth.repositories import (
    AccountRepository,
    DataPassUserRepository,
    PasswordUserRepository,
)
from server.domain.common.types import ID
from server.domain.organizations.exceptions import OrganizationDoesNotExist
from server.domain.organizations.types import Siret
from server.seedwork.application.messages import MessageBus

from .commands import (
    ChangePassword,
    CreateDataPassUser,
    CreatePasswordUser,
    DeletePasswordUser,
)
from .passwords import PasswordEncoder, generate_api_token
from .queries import GetAccountByEmail, LoginDataPassUser, LoginPasswordUser


async def _maybe_reuse_account_of_existing_datapass_user(
    email: str, organization_siret: Siret
) -> Optional[Account]:
    datapass_user_repository = resolve(DataPassUserRepository)

    # Reuse any account tied to an existing DataPassUser.
    datapass_user = await datapass_user_repository.get_by_email(email)

    if datapass_user is None:
        return None

    account = datapass_user.account

    # Ensure the existing account is linked to the same organization.
    # A misconfigured initdata.yml could allow different organizations.
    # See: https://github.com/etalab/catalogage-donnees/issues/414
    if account.organization_siret != organization_siret:
        raise RuntimeError(
            f"Found account for {email=!r} "
            f"in organization {account.organization_siret!r}, "
            "but requested to create a PasswordUser "
            f"in different organization {organization_siret!r}. "
            "HINT: This is most likely an initdata setup issue on the developer side."
        )

    return account


async def create_password_user(
    command: CreatePasswordUser, *, id_: ID = None, role: UserRole = UserRole.USER
) -> ID:
    bus = resolve(MessageBus)

    password_user_repository = resolve(PasswordUserRepository)
    account_repository = resolve(AccountRepository)
    password_encoder = resolve(PasswordEncoder)

    siret = command.organization_siret
    organization = await bus.execute(GetOrganizationBySiret(siret=siret))

    if organization is None:
        raise OrganizationDoesNotExist(siret)

    email = command.email

    account = await _maybe_reuse_account_of_existing_datapass_user(email, siret)

    if account is None:
        account = await account_repository.get_by_email(email)

        if account is not None:
            raise EmailAlreadyExists(email)

        account = Account(
            id=id_ if id_ is not None else account_repository.make_id(),
            organization_siret=command.organization_siret,
            email=email,
            role=role,
            api_token=generate_api_token(),
        )
        await account_repository.insert(account)

    password_hash = password_encoder.hash(command.password)

    password_user = PasswordUser(
        account_id=account.id,
        account=account,
        password_hash=password_hash,
    )

    return await password_user_repository.insert(password_user)


async def delete_password_user(command: DeletePasswordUser) -> None:
    repository = resolve(PasswordUserRepository)
    await repository.delete(command.account_id)


async def login_password_user(query: LoginPasswordUser) -> AuthenticatedAccountView:
    repository = resolve(PasswordUserRepository)
    password_encoder = resolve(PasswordEncoder)

    password_user = await repository.get_by_email(query.email)

    if password_user is None:
        password_encoder.hash(query.password)  # Mitigate timing attacks.
        raise LoginFailed("Invalid credentials")

    if not password_encoder.verify(
        password=query.password, hash=password_user.password_hash
    ):
        raise LoginFailed("Invalid credentials")

    return AuthenticatedAccountView(**password_user.account.dict())


async def create_datapass_user(command: CreateDataPassUser) -> ID:
    datapass_user_repository = resolve(DataPassUserRepository)
    account_repository = resolve(AccountRepository)

    email = command.email

    # Reuse an existing account tied to an existing PasswordUser, or create one.
    account = await account_repository.get_by_email(email)

    # Ensure the existing account is linked to the same organization.
    # A misconfigured initdata.yml used to allow different organizations.
    # See: https://github.com/etalab/catalogage-donnees/issues/414
    if account is not None and account.organization_siret != command.organization_siret:
        raise RuntimeError(
            f"Found account for {email=!r} "
            f"in organization {account.organization_siret!r}, "
            "but requested to create a DataPassUser "
            f"in different organization {command.organization_siret!r}. "
            "HINT: This is most likely a data setup issue on the developer side. "
            "Did you set up a PasswordUser for this email "
            f"in organization {account.organization_siret}? "
        )

    if account is None:
        account = Account(
            id=account_repository.make_id(),
            organization_siret=command.organization_siret,
            email=email,
            role=UserRole.USER,
            api_token=generate_api_token(),
        )
        await account_repository.insert(account)

    datapass_user = await datapass_user_repository.get_by_email(email)

    if datapass_user is not None:
        raise DataPassUserAlreadyExists(account.id)

    datapass_user = DataPassUser(
        account_id=account.id,
        account=account,
    )

    return await datapass_user_repository.insert(datapass_user)


async def login_datapass_user(query: LoginDataPassUser) -> AuthenticatedAccountView:
    repository = resolve(DataPassUserRepository)

    datapass_user = await repository.get_by_email(query.email)

    if datapass_user is None:
        raise LoginFailed("Invalid credentials")

    return AuthenticatedAccountView(**datapass_user.account.dict())


async def get_account_by_email(query: GetAccountByEmail) -> AccountView:
    repository = resolve(AccountRepository)

    email = query.email

    account = await repository.get_by_email(email)

    if account is None:
        raise AccountDoesNotExist(email)

    return AccountView(**account.dict())


async def change_password(command: ChangePassword) -> None:
    repository = resolve(PasswordUserRepository)
    password_encoder = resolve(PasswordEncoder)

    email = command.email
    password_user = await repository.get_by_email(email)

    if password_user is None:
        raise AccountDoesNotExist(email)

    password_user.update_password(password_encoder.hash(command.password))
    password_user.account.update_api_token(generate_api_token())  # Require new login

    await repository.update(password_user)
