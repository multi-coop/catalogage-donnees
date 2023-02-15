from typing import List

from pydantic import Field

from server.domain.extra_fields.entities import ExtraField
from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command

from .validation import CreateCatalogValidationMixin


class CreateCatalog(CreateCatalogValidationMixin, Command[Siret]):
    organization_siret: Siret
    extra_fields: List[ExtraField] = Field(default_factory=list)
