from typing import Any, List

from pydantic import BaseModel, ValidationError, root_validator, validator

from server.domain.catalogs.entities import (
    ExtraField,
    ExtraFieldType,
    parse_extra_fields,
)


class CreateCatalogValidationMixin(BaseModel):
    @validator("extra_fields", check_fields=False, each_item=True, pre=True)
    def convert_extra_fields_type(cls, v: Any) -> dict:
        if isinstance(v, dict) and "type" in v:
            # This may be a string. Ensure Pydantic receives an enum value, as the type
            # annotations are `Literal[ExtraFieldType.<value>]` which Pydantic does not
            # seem to know how to process, contrary to `ExtraFieldType`.
            v["type"] = ExtraFieldType(v["type"])
        return v

    # Fill `organization_siret` both BEFORE (1) and AFTER (2) built-in validation occurs
    # Indeed, depending on the model M used in `extra_fields: List[M]` type annotation,
    # built-in validation may either require it (command entity) or drop it (API schema
    # model).

    # (1)
    @root_validator(pre=True)
    def fill_extra_fields_organization_siret(cls, values: dict) -> dict:
        if "organization_siret" in values:
            for item in values.get("extra_fields", []):
                if isinstance(item, dict):
                    item["organization_siret"] = values["organization_siret"]

        return values

    # (2)
    @validator("extra_fields", check_fields=False)
    def validate_extra_fields(cls, items: list, values: dict) -> List[ExtraField]:
        items = [
            {**item.dict(), "organization_siret": values["organization_siret"]}
            for item in items
        ]

        try:
            return parse_extra_fields(items)
        except ValidationError:
            raise
