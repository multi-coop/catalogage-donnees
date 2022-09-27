import datetime as dt
from typing import List, Optional

from pydantic import BaseModel

from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, UpdateFrequency
from server.domain.datasets.repositories import DatasetHeadlines

from ..catalog_records.views import CatalogRecordView
from ..organizations.views import OrganizationView
from ..tags.views import TagView


class ExtraFieldValueView(BaseModel):
    extra_field_id: ID
    value: str


class DatasetView(BaseModel):
    id: ID
    catalog_record: CatalogRecordView
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

    # Extras
    headlines: Optional[DatasetHeadlines] = None


class DatasetFiltersView(BaseModel):
    organization_siret: List[OrganizationView]
    geographical_coverage: List[str]
    service: List[str]
    format: List[DataFormat]
    technical_source: List[str]
    tag_id: List[TagView]
    license: List[str]
