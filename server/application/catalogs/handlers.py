from typing import Dict, List

from server.config.di import resolve
from server.domain.catalogs.entities import Catalog
from server.domain.catalogs.exceptions import CatalogAlreadyExists, CatalogDoesNotExist
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.common.types import ID, Skip
from server.domain.datasets.repositories import DatasetRepository
from server.domain.datasets.specifications import DatasetSpec
from server.domain.organizations.exceptions import OrganizationDoesNotExist
from server.domain.organizations.repositories import OrganizationRepository
from server.domain.organizations.types import Siret

from .commands import CreateCatalog
from .queries import GetAllCatalogs, GetCatalogBySiret, GetCatalogExport
from .views import CatalogExportView, CatalogView, DatasetExportView


async def get_catalog_by_siret(query: GetCatalogBySiret) -> CatalogView:
    repository = resolve(CatalogRepository)

    siret = query.siret
    catalog = await repository.get_by_siret(siret)

    if catalog is None:
        raise CatalogDoesNotExist(siret)

    return CatalogView(**catalog.dict())


async def get_all_catalogs(
    query: GetAllCatalogs,
) -> List[CatalogView]:
    repository = resolve(CatalogRepository)
    catalogs = await repository.get_all()
    return [CatalogView(**catalog.dict()) for catalog in catalogs]


async def create_catalog(
    command: CreateCatalog, *, extra_field_ids_by_name: Dict[str, ID] = None
) -> Siret:
    repository = resolve(CatalogRepository)
    organization_repository = resolve(OrganizationRepository)

    siret = command.organization_siret
    catalog = await repository.get_by_siret(siret)

    if catalog is not None:
        raise CatalogAlreadyExists(catalog)

    organization = await organization_repository.get_by_siret(siret)

    if organization is None:
        raise OrganizationDoesNotExist(siret)

    extra_fields = command.extra_fields

    if extra_field_ids_by_name is not None:
        for name, id_ in extra_field_ids_by_name.items():
            field = next(field for field in extra_fields if field.name == name)
            field.id = id_

    catalog = Catalog(
        organization=organization,
        extra_fields=extra_fields,
    )

    return await repository.insert(catalog)


async def get_catalog_export(query: GetCatalogExport) -> CatalogExportView:
    repository = resolve(CatalogRepository)
    dataset_repository = resolve(DatasetRepository)

    siret = query.siret
    catalog = await repository.get_by_siret(siret)

    if catalog is None:
        raise CatalogDoesNotExist(siret)

    datasets, _ = await dataset_repository.get_all(
        page=None,
        spec=DatasetSpec(organization_siret=siret),
        account=Skip(),
    )

    return CatalogExportView(
        catalog=CatalogView(**catalog.dict()),
        datasets=[DatasetExportView(**dataset.dict()) for (dataset, _) in datasets],
    )
