from typing import Optional

from server.seedwork.domain.entities import Entity

from .types import Siret


class Organization(Entity):
    name: str
    siret: Siret
    logo_url: Optional[str] = None
