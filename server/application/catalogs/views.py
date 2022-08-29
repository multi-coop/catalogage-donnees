from typing import List

from pydantic import BaseModel

from server.domain.catalogs.entities import ExtraFieldType
from server.domain.common.types import ID
from server.domain.organizations.types import Siret


class ExtraFieldView(BaseModel):
    id: ID
    name: str
    title: str
    hint_text: str
    type: ExtraFieldType
    data: dict


class CatalogView(BaseModel):
    organization_siret: Siret
    extra_fields: List[ExtraFieldView]
