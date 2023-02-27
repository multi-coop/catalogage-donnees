import datetime as dt
from typing import List, Optional

from pydantic import BaseModel

from server.application.dataformats.views import DataFormatView
from server.application.datasets.views import ExtraFieldValueView
from server.application.tags.views import TagView
from server.domain.common.types import ID
from server.domain.datasets.entities import PublicationRestriction, UpdateFrequency
from server.domain.extra_fields.entities import ExtraFieldType

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
    formats: List[DataFormatView]
    technical_source: Optional[str]
    producer_email: Optional[str]
    contact_emails: List[str]
    update_frequency: Optional[UpdateFrequency]
    last_updated_at: Optional[dt.datetime]
    url: Optional[str]
    license: Optional[str]
    tags: List[TagView]
    extra_field_values: List[ExtraFieldValueView]
    publication_restriction: Optional[PublicationRestriction]


class CatalogExportView(BaseModel):
    catalog: CatalogView
    datasets: List[DatasetExportView]
