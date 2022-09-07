from server.domain.catalog_records.entities import CatalogRecord

from ..organizations.transformers import make_entity as make_organization_entity
from .models import CatalogRecordModel


def make_entity(instance: CatalogRecordModel) -> CatalogRecord:
    return CatalogRecord(
        id=instance.id,
        organization=make_organization_entity(instance.catalog.organization),
        created_at=instance.created_at,
    )


def make_instance(entity: CatalogRecord) -> CatalogRecordModel:
    return CatalogRecordModel(
        **entity.dict(
            exclude={
                "organization",
                "created_at",  # Managed by DB for better time consistency
            }
        ),
        organization_siret=entity.organization.siret,
    )
