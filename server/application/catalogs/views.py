from pydantic import BaseModel

from server.domain.organizations.types import Siret


class CatalogView(BaseModel):
    organization_siret: Siret
