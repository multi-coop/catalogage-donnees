from server.domain.catalogs.entities import Catalog

from .models import CatalogModel


def make_entity(instance: CatalogModel) -> Catalog:
    return Catalog(
        organization_siret=instance.organization_siret,
    )


def make_instance(entity: Catalog) -> CatalogModel:
    return CatalogModel(**entity.dict())
