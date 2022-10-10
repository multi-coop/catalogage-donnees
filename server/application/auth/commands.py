from pydantic import EmailStr, SecretStr

from server.domain.common.types import ID
from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command


class CreatePasswordUser(Command[ID]):
    organization_siret: Siret
    email: EmailStr
    password: SecretStr


class CreateDataPassUser(Command[ID]):
    organization_siret: Siret
    email: EmailStr


class DeletePasswordUser(Command[None]):
    account_id: ID


class ChangePassword(Command[None]):
    email: EmailStr
    password: SecretStr
