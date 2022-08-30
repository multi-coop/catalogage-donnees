from pydantic import BaseModel, EmailStr

from server.domain.organizations.types import Siret


class DataPassUserCreate(BaseModel):
    email: EmailStr
    organization_siret: Siret
