from typing import List
from server.domain.common.types import ID
from server.seedwork.domain.repositories import Repository

from .entities import DataFormat


class DataFormatRepository(Repository):
    async def insert(self, entity: DataFormat) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def get_all(self, ids: List[ID] = None) -> List[DataFormat]:
        raise NotImplementedError  # pragma: no cover
