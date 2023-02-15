from typing import List, Optional

from server.seedwork.domain.repositories import Repository

from .entities import ExtraField


class ExtraFieldRepository(Repository):
    async def get_all(self, ids: List[Optional[int]] = None) -> List[ExtraField]:
        raise NotImplementedError  # pragma: no cover
