from ..common.exceptions import DoesNotExist
from .entities import Catalog


class CatalogDoesNotExist(DoesNotExist):
    entity_name = "Catalog"


class CatalogAlreadyExists(Exception):
    def __init__(self, catalog: Catalog) -> None:
        super().__init__()
        self.catalog = catalog
