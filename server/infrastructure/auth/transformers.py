from server.domain.auth.entities import Account, PasswordUser

from .models import AccountModel, PasswordUserModel


def make_account_instance(entity: Account) -> AccountModel:
    return AccountModel(
        id=entity.id,
        organization_siret=entity.organization_siret,
        email=entity.email,
        role=entity.role,
        api_token=entity.api_token,
    )


def make_account_entity(instance: AccountModel) -> Account:
    return Account(
        id=instance.id,
        organization_siret=instance.organization_siret,
        email=instance.email,
        role=instance.role,
        api_token=instance.api_token,
    )


def make_password_user_instance(entity: PasswordUser) -> PasswordUserModel:
    return PasswordUserModel(
        account_id=entity.account_id,
        password_hash=entity.password_hash,
    )


def make_password_user_entity(instance: PasswordUserModel) -> PasswordUser:
    return PasswordUser(
        account_id=instance.account_id,
        account=make_account_entity(instance.account),
        password_hash=instance.password_hash,
    )


def update_instance(instance: PasswordUserModel, entity: PasswordUser) -> None:
    for field in set(PasswordUser.__fields__) - {"account_id", "account"}:
        setattr(instance, field, getattr(entity, field))

    for field in set(Account.__fields__) - {"id"}:
        setattr(instance, field, getattr(entity.account, field))
