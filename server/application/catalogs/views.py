from typing import List

from pydantic import BaseModel

from server.domain.catalogs.entities import ExtraFieldType
from server.domain.common.types import ID

from ..organizations.views import OrganizationView


class ExtraFieldView(BaseModel):
    id: ID
    name: str
    title: str
    hint_text: str
    type: ExtraFieldType
    data: dict


class CatalogView(BaseModel):
    organization: OrganizationView
    extra_fields: List[ExtraFieldView]
