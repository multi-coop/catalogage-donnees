from server.domain.catalogs.entities import (
    Catalog,
    ExtraField,
    ExtraFieldValue,
    parse_extra_field,
)
from server.domain.common.types import ID

from ..organizations.transformers import make_entity as make_organization_entity
from .models import CatalogModel, ExtraFieldModel, ExtraFieldValueModel


def make_entity(instance: CatalogModel) -> Catalog:
    return Catalog(
        organization=make_organization_entity(instance.organization),
        extra_fields=[
            _make_extra_field_entity(extra_field_instance)
            for extra_field_instance in instance.extra_fields
        ],
    )


def make_instance(entity: Catalog) -> CatalogModel:
    return CatalogModel(
        **entity.dict(
            exclude={
                "organization",
                "extra_fields",
            }
        ),
        organization_siret=entity.organization.siret,
        extra_fields=[
            ExtraFieldModel(**extra_field.dict()) for extra_field in entity.extra_fields
        ]
    )


def _make_extra_field_entity(instance: ExtraFieldModel) -> ExtraField:
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
