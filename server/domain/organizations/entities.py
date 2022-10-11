from server.seedwork.domain.entities import Entity

from .types import Siret


class Organization(Entity):
    name: str
    siret: Siret
