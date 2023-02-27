from typing import Union

from pydantic import BaseModel

from server.domain.common.types import ID
from server.domain.extra_fields.entities import (
    ExtraFieldType,
    _BoolExtraFieldData,
    _EnumExtraFieldData,
)
from server.domain.organizations.types import Siret


class ExtraFieldView(BaseModel):
    id: ID
    organization_siret: Siret
    name: str
    title: str
    hint_text: str
    data: Union[_BoolExtraFieldData, _EnumExtraFieldData, dict]
    type: ExtraFieldType
