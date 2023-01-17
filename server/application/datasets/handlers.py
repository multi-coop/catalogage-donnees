from server.application.catalogs.queries import GetAllCatalogs
from server.application.licenses.queries import GetLicenseSet
from server.application.tags.queries import GetAllTags
from server.config.di import resolve
from server.domain.catalog_records.entities import CatalogRecord
from server.domain.catalog_records.repositories import CatalogRecordRepository
from server.domain.catalogs.exceptions import CatalogDoesNotExist
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.common.pagination import Pagination
from server.domain.common.types import ID, Skip
from server.domain.dataformats.repositories import DataFormatRepository
from server.domain.datasets.entities import Dataset
from server.domain.datasets.exceptions import DatasetDoesNotExist
from server.domain.datasets.repositories import DatasetRepository
from server.domain.organizations.types import Siret
from server.domain.tags.repositories import TagRepository
from server.seedwork.application.messages import MessageBus

from .commands import CreateDataset, DeleteDataset, UpdateDataset
from .exceptions import CannotCreateDataset, CannotSeeDataset, CannotUpdateDataset
from .queries import GetAllDatasets, GetDatasetByID, GetDatasetFilters
from .specifications import (
    can_create_dataset,
    can_not_change_publication_restriction_level,
    can_see_dataset,
    can_update_dataset,
)
from .views import DatasetFiltersView, DatasetView

# This organization typically holds password users used by the development team.
# It is created by migration `f2ef4eef61e3` (create-legacy-organization).
_LEGACY_ORGANIZATION_SIRET = Siret("000 000 000 00000")


async def create_dataset(command: CreateDataset, *, id_: ID = None) -> ID:
    repository = resolve(DatasetRepository)
    catalog_repository = resolve(CatalogRepository)
    catalog_record_repository = resolve(CatalogRecordRepository)
    tag_repository = resolve(TagRepository)
    format_repository = resolve(DataFormatRepository)

    if id_ is None:
        id_ = repository.make_id()

    catalog = await catalog_repository.get_by_siret(siret=command.organization_siret)

    if catalog is None:
        raise CatalogDoesNotExist(command.organization_siret)

    if not isinstance(command.account, Skip) and not can_create_dataset(
        catalog, command.account
    ):
        raise CannotCreateDataset(
            f"{command.account.organization_siret=}, {catalog.organization.siret=}"
        )

    catalog_record_id = await catalog_record_repository.insert(
        CatalogRecord(
            id=catalog_record_repository.make_id(),
            organization=catalog.organization,
        )
    )
    catalog_record = await catalog_record_repository.get_by_id(catalog_record_id)
    assert catalog_record is not None

    tags = await tag_repository.get_all(ids=command.tag_ids)

    formats = await format_repository.get_all(ids=command.format_ids)

    dataset = Dataset(
        id=id_,
        catalog_record=catalog_record,
        tags=tags,
        formats=formats,
        **command.dict(exclude={"tag_ids", "format_ids"}),
    )

    return await repository.insert(dataset)


async def update_dataset(command: UpdateDataset) -> None:
    repository = resolve(DatasetRepository)
    tag_repository = resolve(TagRepository)
    format_repository = resolve(DataFormatRepository)

    pk = command.id
    dataset = await repository.get_by_id(pk)
    if dataset is None:
        raise DatasetDoesNotExist(pk)

    if not isinstance(command.account, Skip) and not can_update_dataset(
        dataset, command.account
    ):
        raise CannotUpdateDataset(f"{command.account=}, {dataset=}")

    if (
        not isinstance(command.account, Skip)
        and command.publication_restriction is not None
        and can_not_change_publication_restriction_level(
            dataset=dataset,
            account=command.account,
            new_publication_restriction_level=command.publication_restriction,
        )
    ):
        raise CannotUpdateDataset(f"{command.account=}, {dataset=}")

    tags = await tag_repository.get_all(ids=command.tag_ids)
    formats = await format_repository.get_all(ids=command.format_ids)

    dataset.update(
        **command.dict(
            exclude={"account", "id", "tag_ids", "format_ids", "extra_field_values"}
        ),
        tags=tags,
        formats=formats,
        extra_field_values=command.extra_field_values,
    )

    await repository.update(dataset)


async def delete_dataset(command: DeleteDataset) -> None:
    repository = resolve(DatasetRepository)
    await repository.delete(command.id)


async def get_dataset_filters(query: GetDatasetFilters) -> DatasetFiltersView:
    bus = resolve(MessageBus)
    repository = resolve(DatasetRepository)
    data_format_repository = resolve(DataFormatRepository)

    catalogs = await bus.execute(GetAllCatalogs())
    geographical_coverages = await repository.get_geographical_coverage_set()
    services = await repository.get_service_set()
    technical_sources = await repository.get_technical_source_set()
    tags = await bus.execute(GetAllTags())
    formats = await data_format_repository.get_all()
    licenses = await bus.execute(GetLicenseSet())

    return DatasetFiltersView(
        organization_siret=[
            catalog.organization
            for catalog in catalogs
            if catalog.organization.siret != _LEGACY_ORGANIZATION_SIRET
        ],
        geographical_coverage=sorted(geographical_coverages),
        service=list(services),
        format_id=formats,
        technical_source=list(technical_sources),
        tag_id=tags,
        license=["*", *licenses],
    )


async def get_all_datasets(query: GetAllDatasets) -> Pagination[DatasetView]:
    dataset_repository = resolve(DatasetRepository)

    datasets, count = await dataset_repository.get_all(
        page=query.page, spec=query.spec, account=query.account
    )

    views = [DatasetView(**dataset.dict(), **extras) for dataset, extras in datasets]

    return Pagination(items=views, total_items=count, page_size=query.page.size)


async def get_dataset_by_id(query: GetDatasetByID) -> DatasetView:
    repository = resolve(DatasetRepository)
    id = query.id
    dataset = await repository.get_by_id(id)

    if dataset is None:
        raise DatasetDoesNotExist(id)

    if not isinstance(query.account, Skip) and not can_see_dataset(
        dataset, query.account
    ):
        raise CannotSeeDataset(f"{query.account.organization_siret=}, {id=}")

    return DatasetView(**dataset.dict())
