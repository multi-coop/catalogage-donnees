from server.config.di import resolve
from server.domain.catalogs.entities import Catalog
from server.domain.catalogs.exceptions import CatalogAlreadyExists, CatalogDoesNotExist
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.organizations.types import Siret

from .commands import CreateCatalog
from .queries import GetCatalogBySiret
from .views import CatalogView


async def get_catalog_by_siret(query: GetCatalogBySiret) -> CatalogView:
    repository = resolve(CatalogRepository)

    siret = query.siret
    catalog = await repository.get_by_siret(siret)

    if catalog is None:
        raise CatalogDoesNotExist(siret)

    return CatalogView(**catalog.dict())


async def create_catalog(command: CreateCatalog) -> Siret:
    repository = resolve(CatalogRepository)

    siret = command.organization_siret
    catalog = await repository.get_by_siret(siret)

    if catalog is not None:
        raise CatalogAlreadyExists(catalog)

    catalog = Catalog(
        organization_siret=siret,
        extra_fields=command.extra_fields,
    )

    return await repository.insert(catalog)
