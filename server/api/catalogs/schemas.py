from typing import List

from pydantic import BaseModel, Field

from server.application.catalogs.validation import CreateCatalogValidationMixin
from server.domain.catalogs.entities import ExtraFieldType
from server.domain.common.types import ID
from server.domain.organizations.types import Siret


class ExtraFieldCreate(BaseModel):
    name: str
    title: str
    hint_text: str
    type: ExtraFieldType
    data: dict = Field(default_factory=dict)


class CatalogCreate(CreateCatalogValidationMixin, BaseModel):
    organization_siret: Siret
    extra_fields: List[ExtraFieldCreate] = Field(default_factory=list)


class ExtraFieldValueCreate(BaseModel):
    extra_field_id: ID
    value: str
