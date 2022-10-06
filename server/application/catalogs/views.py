import csv
import datetime as dt
import json
from typing import List, Optional, TextIO

from pydantic import BaseModel

from server.application.datasets.views import ExtraFieldValueView
from server.application.tags.views import TagView
from server.domain.catalogs.entities import ExtraFieldType
from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, UpdateFrequency

from ..organizations.views import OrganizationView


class ExtraFieldView(BaseModel):
    id: ID
    name: str
    title: str
    hint_text: str
    type: ExtraFieldType
    data: dict


class CatalogView(BaseModel):
    organization: OrganizationView
    extra_fields: List[ExtraFieldView]


class DatasetExportView(BaseModel):
    title: str
    description: str
    service: str
    geographical_coverage: str
    formats: List[DataFormat]
    technical_source: Optional[str]
    producer_email: Optional[str]
    contact_emails: List[str]
    update_frequency: Optional[UpdateFrequency]
    last_updated_at: Optional[dt.datetime]
    url: Optional[str]
    license: Optional[str]
    tags: List[TagView]
    extra_field_values: List[ExtraFieldValueView]


class CatalogExportView(BaseModel):
    catalog: CatalogView
    datasets: List[DatasetExportView]

    def to_csv(self, f: TextIO) -> None:
        fieldnames: List[str] = []

        fieldnames.extend(
            key
            for key in DatasetExportView.__fields__.keys()
            if key != "extra_field_values"
        )

        fieldnames.extend(extra_field.name for extra_field in self.catalog.extra_fields)

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for dataset in self.datasets:
            # TODO: convert
            row = json.loads(dataset.json(exclude={"extra_field_values"}))

            extra_field_value_by_id = {
                extra_field_value.extra_field_id: extra_field_value.value
                for extra_field_value in dataset.extra_field_values
            }

            for extra_field in self.catalog.extra_fields:
                row[extra_field.name] = extra_field_value_by_id.get(extra_field.id, "")

            writer.writerow(row)
