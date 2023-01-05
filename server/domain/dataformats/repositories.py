from typing import List, Optional

from server.seedwork.domain.repositories import Repository

from .entities import DataFormat


class DataFormatRepository(Repository):
    async def insert(self, entity: DataFormat) -> Optional[int]:
        raise NotImplementedError  # pragma: no cover

    async def get_all(self, ids: List[int] = None) -> List[DataFormat]:
        raise NotImplementedError  # pragma: no cover
