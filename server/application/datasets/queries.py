from typing import Union

from server.domain.auth.entities import Account
from server.domain.common.pagination import Page, Pagination
from server.domain.common.types import ID, Skip
from server.domain.datasets.specifications import DatasetSpec
from server.seedwork.application.queries import Query

from .views import DatasetFiltersView, DatasetView


class GetAllDatasets(Query[Pagination[DatasetView]]):
    page: Page = Page()
    spec: DatasetSpec = DatasetSpec()
    account: Union[Account, Skip] = Skip()


class GetDatasetByID(Query[DatasetView]):
    id: ID
    account: Union[Account, Skip]


class GetDatasetFilters(Query[DatasetFiltersView]):
    pass
