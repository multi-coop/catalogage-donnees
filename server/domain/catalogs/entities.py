from typing import List

from pydantic import Field
from typing_extensions import Annotated

from server.domain.extra_fields.entities import ExtraField
from server.seedwork.domain.entities import Entity

from ..organizations.entities import Organization


class Catalog(Entity):
    organization: Organization
    extra_fields: List[Annotated[ExtraField, Field(discriminator="type")]]
