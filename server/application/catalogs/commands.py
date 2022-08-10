from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command


class CreateCatalog(Command[Siret]):
    organization_siret: Siret
