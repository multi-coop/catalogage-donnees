from server.application.catalogs.commands import CreateCatalog
from server.application.catalogs.handlers import (
    create_catalog,
    get_all_catalogs,
    get_catalog_by_siret,
)
from server.application.catalogs.queries import GetAllCatalogs, GetCatalogBySiret
from server.seedwork.application.modules import Module


class CatalogsModule(Module):
    command_handlers = {
        CreateCatalog: create_catalog,
    }

    query_handlers = {
        GetCatalogBySiret: get_catalog_by_siret,
        GetAllCatalogs: get_all_catalogs,
    }
