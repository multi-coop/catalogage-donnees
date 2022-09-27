from server.domain.auth.entities import Account
from server.domain.catalogs.entities import Catalog


def can_create_dataset(catalog: Catalog, account: Account) -> bool:
    return catalog.organization.siret == account.organization_siret
