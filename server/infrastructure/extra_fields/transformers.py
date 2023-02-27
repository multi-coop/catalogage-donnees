from server.domain.common.types import ID
from server.domain.extra_fields.entities import (
    ExtraField,
    ExtraFieldValue,
    parse_extra_field,
)

from .models import ExtraFieldModel, ExtraFieldValueModel


def make_entity(instance: ExtraFieldModel) -> ExtraField:
    kwargs = {
        field: getattr(instance, field)
        for field in (
            "id",
            "organization_siret",
            "name",
            "title",
            "hint_text",
            "type",
            "data",
        )
    }

    return parse_extra_field(kwargs)  # type: ignore


def make_extra_field_value_entity(instance: ExtraFieldValueModel) -> ExtraFieldValue:
    return ExtraFieldValue(
        extra_field_id=instance.extra_field_id,
        value=instance.value,
    )


def make_extra_field_value_instance(
    entity: ExtraFieldValue, dataset_id: ID
) -> ExtraFieldValueModel:
    return ExtraFieldValueModel(
        dataset_id=dataset_id,
        extra_field_id=entity.extra_field_id,
        value=entity.value,
    )
