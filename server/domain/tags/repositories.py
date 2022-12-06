from typing import List, Optional

from server.domain.common.types import ID, id_factory
from server.seedwork.domain.repositories import Repository

from .entities import Tag


class TagRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_all(self, *, ids: List[ID] = None) -> List[Tag]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_id(self, id_: ID) -> Optional[Tag]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Tag) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def delete_by_id(self, id_: ID) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def delete_many_by_id(self, ids_: List[ID]) -> List[ID]:
        raise NotImplementedError  # pragma: no cover
