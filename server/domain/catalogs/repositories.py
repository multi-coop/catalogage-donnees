from typing import Optional

from server.seedwork.domain.repositories import Repository

from ..organizations.types import Siret
from .entities import Catalog


class CatalogRepository(Repository):
    async def get_by_siret(self, siret: Siret) -> Optional[Catalog]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, catalog: Catalog) -> Siret:
        raise NotImplementedError  # pragma: no cover
