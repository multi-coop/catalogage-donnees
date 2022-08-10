from pydantic import BaseModel

from server.domain.organizations.types import Siret


class CatalogCreate(BaseModel):
    organization_siret: Siret
