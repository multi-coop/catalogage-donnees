from typing import List

from server.seedwork.domain.repositories import Repository

from .entities import ExtraField


class ExtraFieldRepository(Repository):
    async def get_all(self, organization_siret: str) -> List[ExtraField]:
        raise NotImplementedError  # pragma: no cover
