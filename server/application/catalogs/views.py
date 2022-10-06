import csv
import datetime as dt
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
        fieldnames = [
            "titre",
            "description",
            "service",
            "couv_geo",
            "format",
            "si",
            "contact_service",
            "contact_personne",
            "freq_maj",
            "date_maj",
            "url",
            "licence",
            "mots_cles"
        ]

        fieldnames.extend(extra_field.name for extra_field in self.catalog.extra_fields)

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for dataset in self.datasets:
            row = {
                "titre": dataset.title,
                "description": dataset.description,
                "service": dataset.service,
                "couv_geo": dataset.geographical_coverage,
                "format": ", ".join(fmt.value for fmt in dataset.formats),
                "si": dataset.technical_source or "",
                "contact_service": dataset.producer_email or "",
                "contact_personne": ", ".join(dataset.contact_emails),
                "freq_maj": (
                    freq.value if (freq := dataset.update_frequency) is not None else ""
                ),
                "date_maj": (
                    d.strftime("%d/%M/%Y")
                    if (d := dataset.last_updated_at) is not None
                    else ""
                ),
                "url": dataset.url or "",
                "licence": dataset.license or "",
                "mots_cles": ", ".join(tag.name for tag in dataset.tags),
            }

            extra_field_value_by_id = {
                extra_field_value.extra_field_id: extra_field_value.value
                for extra_field_value in dataset.extra_field_values
            }

            for extra_field in self.catalog.extra_fields:
                row[extra_field.name] = extra_field_value_by_id.get(extra_field.id, "")

            writer.writerow(row)
