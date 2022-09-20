from server.domain.auth.entities import Account, UserRole
from server.domain.catalogs.entities import Catalog


def can_create_dataset(catalog: Catalog, account: Account) -> bool:
    if account.role == UserRole.ADMIN:
        return True

    return catalog.organization.siret == account.organization_siret
