import datetime as dt
import enum
from typing import List, Optional

from pydantic import Field

from server.domain.catalogs.entities import ExtraFieldValue
from server.domain.tags.entities import Tag
from server.seedwork.domain.entities import Entity

from ..catalog_records.entities import CatalogRecord
from ..common.types import ID


class DataFormat(enum.Enum):
    FILE_TABULAR = "file_tabular"
    FILE_GIS = "file_gis"
    API = "api"
    DATABASE = "database"
    WEBSITE = "website"
    OTHER = "other"


class UpdateFrequency(enum.Enum):
    NEVER = "never"
    REALTIME = "realtime"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class PublicationRestriction(enum.Enum):
    DRAFT = "draft"  # the dataset is a draft
    LEGAL_RESTRICTION = (
        "legal_restriction"  # the dataset is not published for legal reason
    )
    NO_RESTRICTION = "no_restriction"  # the dataset has no publication restriction


class Dataset(Entity):
    id: ID
    catalog_record: CatalogRecord
    title: str
    description: str
    service: str
    geographical_coverage: str
    formats: List[DataFormat]
    technical_source: Optional[str]
    producer_email: Optional[str]
    contact_emails: List[str]
    update_frequency: Optional[UpdateFrequency] = None
    publication_restriction: Optional[
        PublicationRestriction
    ] = PublicationRestriction.NO_RESTRICTION
    last_updated_at: Optional[dt.datetime] = None
    url: Optional[str] = None
    license: Optional[str] = None
    tags: List[Tag] = Field(default_factory=list)
    extra_field_values: List[ExtraFieldValue] = Field(default_factory=list)

    class Config:
        orm_mode = True

    def update(
        self,
        title: str,
        description: str,
        service: str,
        geographical_coverage: str,
        formats: List[DataFormat],
        technical_source: Optional[str],
        producer_email: Optional[str],
        contact_emails: List[str],
        update_frequency: Optional[UpdateFrequency],
        last_updated_at: Optional[dt.datetime],
        url: Optional[str],
        license: Optional[str],
        tags: List[Tag],
        extra_field_values: List[ExtraFieldValue],
        publication_restriction: Optional[PublicationRestriction],
    ) -> None:
        self.title = title
        self.description = description
        self.service = service
        self.geographical_coverage = geographical_coverage
        self.formats = formats
        self.technical_source = technical_source
        self.producer_email = producer_email
        self.contact_emails = contact_emails
        self.update_frequency = update_frequency
        self.last_updated_at = last_updated_at
        self.url = url
        self.license = license
        self.tags = tags
        self.extra_field_values = extra_field_values
        self.publication_restriction = publication_restriction
