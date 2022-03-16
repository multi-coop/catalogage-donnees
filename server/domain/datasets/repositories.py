from typing import List, Optional, Tuple

from typing_extensions import TypedDict

from server.seedwork.domain.repositories import Repository

from ..common.types import ID, id_factory
from .entities import Dataset


class DatasetHeadlines(TypedDict):
    title: str
    description: str


class DatasetRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_all(self) -> List[Dataset]:
        raise NotImplementedError  # pragma: no cover

    async def search(
        self, q: str, highlight: bool = False
    ) -> List[Tuple[Dataset, Optional[DatasetHeadlines]]]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Dataset) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def update(self, entity: Dataset) -> None:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, id: ID) -> None:
        raise NotImplementedError  # pragma: no cover
