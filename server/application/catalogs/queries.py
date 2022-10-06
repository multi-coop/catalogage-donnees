from typing import List

from server.domain.organizations.types import Siret
from server.seedwork.application.queries import Query

from .views import CatalogExportView, CatalogView


class GetCatalogBySiret(Query[CatalogView]):
    siret: Siret


class GetAllCatalogs(Query[List[CatalogView]]):
    pass

class GetCatalogExport(Query[CatalogExportView]):
    siret: Siret