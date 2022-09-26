from typing import List

from server.domain.organizations.types import Siret
from server.seedwork.application.queries import Query

from .views import CatalogView


class GetCatalogBySiret(Query[CatalogView]):
    siret: Siret


class GetAllNonEmptyCatalogs(Query[List[CatalogView]]):
    pass
