from server.seedwork.domain.entities import Entity

from .types import Siret


class Organization(Entity):
    name: str
    siret: Siret


# This organization holds legacy users. Its catalog holds legacy datasets.
# "Legacy" means "prior to multi-org system powered by DataPass".
# Going forward SIRET numbers will come from DataPass via the user's organization(s).
LEGACY_ORGANIZATION = Organization(
    name="Organisation par défaut", siret=Siret("000 000 000 00000")
)
