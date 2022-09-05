from typing import List

from server.domain.datasets.entities import Dataset

from ..catalog_records.models import CatalogRecordModel
from ..catalog_records.transformers import make_entity as make_catalog_record_entity
from ..catalogs.transformers import (
    make_extra_field_value_entity,
    make_extra_field_value_instance,
)
from ..tags.models import TagModel
from ..tags.transformers import make_entity as make_tag_entity
from .models import DataFormatModel, DatasetModel


def make_entity(instance: DatasetModel) -> Dataset:
    kwargs: dict = {
        "catalog_record": make_catalog_record_entity(instance.catalog_record),
        "formats": [fmt.name for fmt in instance.formats],
        "tags": [make_tag_entity(tag) for tag in instance.tags],
        "extra_field_values": [
            make_extra_field_value_entity(value)
            for value in instance.extra_field_values
        ],
    }

    kwargs.update(
        (field, getattr(instance, field))
        for field in Dataset.__fields__
        if field not in kwargs
    )

    return Dataset(**kwargs)


def make_instance(
    entity: Dataset,
    catalog_record: CatalogRecordModel,
    formats: List[DataFormatModel],
    tags: List[TagModel],
) -> DatasetModel:
    instance = DatasetModel(
        **entity.dict(
            exclude={"catalog_record", "formats", "tags", "extra_field_values"}
        ),
    )

    instance.catalog_record = catalog_record
    instance.formats = formats
    instance.tags = tags
    instance.extra_field_values = [
        make_extra_field_value_instance(value, dataset_id=entity.id)
        for value in entity.extra_field_values
    ]

    return instance


def update_instance(
    instance: DatasetModel,
    entity: Dataset,
    formats: List[DataFormatModel],
    tags: List[TagModel],
) -> None:
    for field in set(Dataset.__fields__) - {
        "id",
        "catalog_record",
        "formats",
        "tags",
        "extra_field_values",
    }:
        setattr(instance, field, getattr(entity, field))

    instance.formats = formats
    instance.tags = tags
    instance.extra_field_values = [
        make_extra_field_value_instance(value, dataset_id=entity.id)
        for value in entity.extra_field_values
    ]
