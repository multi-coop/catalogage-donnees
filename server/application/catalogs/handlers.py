from typing import Dict

from server.config.di import resolve
from server.domain.catalogs.entities import Catalog
from server.domain.catalogs.exceptions import CatalogAlreadyExists, CatalogDoesNotExist
from server.domain.catalogs.repositories import CatalogRepository
from server.domain.common.types import ID
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


async def create_catalog(
    command: CreateCatalog, extra_field_ids_by_name: Dict[str, ID] = None
) -> Siret:
    repository = resolve(CatalogRepository)

    siret = command.organization_siret
    catalog = await repository.get_by_siret(siret)

    if catalog is not None:
        raise CatalogAlreadyExists(catalog)

    extra_fields = command.extra_fields

    if extra_field_ids_by_name is not None:
        for name, id_ in extra_field_ids_by_name.items():
            field = next(field for field in extra_fields if field.name == name)
            field.id = id_

    catalog = Catalog(
        organization_siret=siret,
        extra_fields=extra_fields,
    )

    return await repository.insert(catalog)
