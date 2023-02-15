from server.domain.catalogs.entities import Catalog
from server.infrastructure.extra_fields.models import ExtraFieldModel

from ..extra_fields.transformers import make_entity as make_extra_field_entity
from ..organizations.transformers import make_entity as make_organization_entity
from .models import CatalogModel


def make_entity(instance: CatalogModel) -> Catalog:
    return Catalog(
        organization=make_organization_entity(instance.organization),
        extra_fields=[
            make_extra_field_entity(extra_field_instance)
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
