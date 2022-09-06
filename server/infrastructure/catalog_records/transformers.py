from server.domain.catalog_records.entities import CatalogRecord

from .models import CatalogRecordModel


def make_entity(instance: CatalogRecordModel) -> CatalogRecord:
    return CatalogRecord(
        id=instance.id,
        organization_siret=instance.organization_siret,
        created_at=instance.created_at,
    )


def make_instance(entity: CatalogRecord) -> CatalogRecordModel:
    return CatalogRecordModel(
        **entity.dict(
            exclude={
                "created_at",  # Managed by DB for better time consistency
            }
        ),
    )
