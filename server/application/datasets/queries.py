from typing import List, Optional, Union

from server.domain.auth.entities import Account
from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID, Skip
from server.domain.datasets.specifications import DatasetSpec
from server.seedwork.application.queries import Query

from .views import DatasetFiltersView, DatasetView


class GetAllDatasets(Query[Pagination[DatasetView]]):
    page: Page = Page()
    spec: DatasetSpec = DatasetSpec()


class GetDatasetByID(Query[DatasetView]):
    account: Union[Account, Skip]
    id: ID


class GetDatasetFilters(Query[DatasetFiltersView]):
    pass
