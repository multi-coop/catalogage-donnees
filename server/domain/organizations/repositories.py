from typing import Optional, Set

from server.domain.organizations.types import Siret
from server.seedwork.domain.repositories import Repository

from .entities import Organization


class OrganizationRepository(Repository):
    async def get_by_siret(self, siret: Siret) -> Optional[Organization]:
        raise NotImplementedError  # pragma: no cover

    async def get_siret_set(self) -> Set[Siret]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Organization) -> Siret:
        raise NotImplementedError  # pragma: no cover
