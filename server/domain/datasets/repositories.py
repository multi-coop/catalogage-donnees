from typing import List, Optional, Set, Tuple

from typing_extensions import TypedDict

from server.seedwork.domain.repositories import Repository

from ..common.pagination import Page
from ..common.types import ID, id_factory
from .entities import Dataset
from .specifications import DatasetSpec


class DatasetHeadlines(TypedDict):
    title: str
    description: Optional[str]


class DatasetGetAllExtras(TypedDict, total=False):
    headlines: DatasetHeadlines


class DatasetRepository(Repository):
    def make_id(self) -> ID:
        return id_factory()

    async def get_all(
        self, *, page: Optional[Page] = Page(), spec: DatasetSpec = DatasetSpec()
    ) -> Tuple[List[Tuple[Dataset, DatasetGetAllExtras]], int]:
        raise NotImplementedError  # pragma: no cover

    async def get_by_id(self, id: ID) -> Optional[Dataset]:
        raise NotImplementedError  # pragma: no cover

    async def get_geographical_coverage_set(self) -> Set[str]:
        raise NotImplementedError  # pragma: no cover

    async def get_service_set(self) -> Set[str]:
        raise NotImplementedError  # pragma: no cover

    async def get_technical_source_set(self) -> Set[str]:
        raise NotImplementedError  # pragma: no cover

    async def get_license_set(self) -> Set[str]:
        raise NotImplementedError  # pragma: no cover

    async def insert(self, entity: Dataset) -> ID:
        raise NotImplementedError  # pragma: no cover

    async def update(self, entity: Dataset) -> None:
        raise NotImplementedError  # pragma: no cover

    async def delete(self, id: ID) -> None:
        raise NotImplementedError  # pragma: no cover
