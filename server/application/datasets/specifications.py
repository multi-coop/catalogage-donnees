from server.domain.auth.entities import Account
from server.domain.catalogs.entities import Catalog
from server.domain.datasets.entities import Dataset


def can_create_dataset(catalog: Catalog, account: Account) -> bool:
    return catalog.organization.siret == account.organization_siret


def can_update_dataset(dataset: Dataset, account: Account) -> bool:
    return dataset.catalog_record.organization.siret == account.organization_siret
