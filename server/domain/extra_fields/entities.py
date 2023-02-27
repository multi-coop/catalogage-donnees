from enum import Enum
from typing import Any, List, Literal, Union

from pydantic import BaseModel, Field, parse_obj_as
from typing_extensions import Annotated, TypedDict

from server.domain.common.types import ID, id_factory
from server.seedwork.domain.entities import Entity

from ..organizations.types import Siret


class ExtraFieldType(Enum):
    TEXT = "TEXT"
    ENUM = "ENUM"
    BOOL = "BOOL"


class _ExtraFieldBase(BaseModel):
    id: ID = Field(default_factory=id_factory)
    organization_siret: Siret
    name: str
    title: str
    hint_text: str


class TextExtraField(_ExtraFieldBase, Entity):
    type: Literal[ExtraFieldType.TEXT] = ExtraFieldType.TEXT
    data: dict = {}


class _EnumExtraFieldData(TypedDict):
    values: List[str]


class EnumExtraField(_ExtraFieldBase, Entity):
    type: Literal[ExtraFieldType.ENUM] = ExtraFieldType.ENUM
    data: _EnumExtraFieldData


class _BoolExtraFieldData(TypedDict):
    true_value: str
    false_value: str


class BoolExtraField(_ExtraFieldBase, Entity):
    type: Literal[ExtraFieldType.BOOL] = ExtraFieldType.BOOL
    data: _BoolExtraFieldData


# See: https://pydantic-docs.helpmanual.io/usage/types/#discriminated-unions-aka-tagged-unions  # noqa: E501
ExtraField = Union[TextExtraField, EnumExtraField, BoolExtraField]


def parse_extra_field(item: Any) -> ExtraField:
    return parse_obj_as(ExtraField, item)  # type: ignore


def parse_extra_fields(items: list) -> List[ExtraField]:
    return parse_obj_as(List[Annotated[ExtraField, Field(discriminator="type")]], items)


class ExtraFieldValue(Entity):
    extra_field_id: ID
    value: str
