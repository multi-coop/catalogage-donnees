from typing import Optional

from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command


class CreateOrganization(Command[Siret]):
    name: str
    siret: Siret
    logo_url: Optional[str] = None
