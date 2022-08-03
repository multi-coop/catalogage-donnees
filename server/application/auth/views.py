from pydantic import BaseModel

from server.domain.auth.entities import UserRole
from server.domain.common.types import ID
from server.domain.organizations.types import Siret


class AccountView(BaseModel):
    id: ID
    organization_siret: Siret
    email: str
    role: UserRole


class AuthenticatedAccountView(BaseModel):
    id: ID
    organization_siret: Siret
    email: str
    role: UserRole
    api_token: str
