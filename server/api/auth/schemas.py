from pydantic import BaseModel, EmailStr, SecretStr

from server.domain.organizations.types import Siret


class PasswordUserCreate(BaseModel):
    organization_siret: Siret
    email: EmailStr
    password: SecretStr


class PasswordUserLogin(BaseModel):
    email: EmailStr
    password: SecretStr
