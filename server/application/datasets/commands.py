import datetime as dt
from typing import List, Optional, Union

from pydantic import EmailStr, Field

from server.domain.auth.entities import Account
from server.domain.catalogs.entities import ExtraFieldValue
from server.domain.common.types import ID, Skip
from server.domain.datasets.entities import PublicationRestriction, UpdateFrequency
from server.domain.organizations.types import Siret
from server.seedwork.application.commands import Command

from .validation import CreateDatasetValidationMixin, UpdateDatasetValidationMixin


class CreateDataset(CreateDatasetValidationMixin, Command[ID]):
    account: Union[Account, Skip]

    organization_siret: Siret
    title: str
    description: str
    service: str
    geographical_coverage: str
    format_ids: List[int]
    technical_source: Optional[str] = None
    producer_email: Optional[EmailStr] = None
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = None
    last_updated_at: Optional[dt.datetime] = None
    url: Optional[str] = None
    license: Optional[str] = None
    tag_ids: List[ID] = Field(default_factory=list)
    extra_field_values: List[ExtraFieldValue] = Field(default_factory=list)
    publication_restriction: Optional[
        PublicationRestriction
    ] = PublicationRestriction.NO_RESTRICTION


class UpdateDataset(UpdateDatasetValidationMixin, Command[None]):
    account: Union[Account, Skip]

    id: ID
    title: str
    description: str
    service: str
    geographical_coverage: str
    formats: List[str]
    technical_source: Optional[str] = Field(...)
    producer_email: Optional[EmailStr] = Field(...)
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = Field(...)
    last_updated_at: Optional[dt.datetime] = Field(...)
    url: Optional[str] = Field(...)
    license: Optional[str] = Field(...)
    tag_ids: List[ID]
    extra_field_values: List[ExtraFieldValue]
    publication_restriction: Optional[PublicationRestriction] = Field(...)


class DeleteDataset(Command[None]):
    id: ID
