import datetime as dt
from typing import List, Optional

from pydantic import EmailStr, Field

from server.domain.catalogs.entities import ExtraFieldValue
from server.domain.common.types import ID
from server.domain.datasets.entities import DataFormat, UpdateFrequency
from server.domain.organizations.entities import LEGACY_ORGANIZATION_SIRET
from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command

from .validation import CreateDatasetValidationMixin, UpdateDatasetValidationMixin


class CreateDataset(CreateDatasetValidationMixin, Command[ID]):
    organization_siret: Siret = LEGACY_ORGANIZATION_SIRET
    title: str
    description: str
    service: str
    geographical_coverage: str
    formats: List[DataFormat]
    technical_source: Optional[str] = None
    producer_email: Optional[EmailStr] = None
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None
    url: Optional[str] = None
    license: Optional[str] = None
    tag_ids: List[ID] = Field(default_factory=list)
    extra_field_values: List[ExtraFieldValue] = Field(default_factory=list)


class UpdateDataset(UpdateDatasetValidationMixin, Command[None]):
    id: ID
    title: str
    description: str
    service: str
    geographical_coverage: str
    formats: List[DataFormat]
    technical_source: Optional[str] = Field(...)
    producer_email: Optional[EmailStr] = Field(...)
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = Field(...)
    last_updated_at: Optional[dt.datetime] = Field(...)
    url: Optional[str] = Field(...)
    license: Optional[str] = Field(...)
    tag_ids: List[ID]
    extra_field_values: List[ExtraFieldValue]


class DeleteDataset(Command[None]):
    id: ID
