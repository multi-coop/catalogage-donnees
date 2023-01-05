import datetime as dt
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field

from server.api.catalogs.schemas import ExtraFieldValueCreate
from server.application.datasets.validation import (
    CreateDatasetValidationMixin,
    UpdateDatasetValidationMixin,
)
from server.domain.common.types import ID
from server.domain.datasets.entities import PublicationRestriction, UpdateFrequency
from server.domain.organizations.types import Siret


class DatasetListParams:
    def __init__(
        self,
        q: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 10,
        organization_siret: Optional[Siret] = Query(None),
        geographical_coverage: Optional[List[str]] = Query(None),
        service: Optional[List[str]] = Query(None),
        format_: Optional[List[str]] = Query(None, alias="format"),
        technical_source: Optional[List[str]] = Query(None),
        tag_id: Optional[List[ID]] = Query(None),
        license: Optional[str] = Query(None),
        publication_restriction: Optional[PublicationRestriction] = Query(None),
    ) -> None:
        self.q = q
        self.organization_siret = organization_siret
        self.page_number = page_number
        self.page_size = page_size
        self.geographical_coverage = geographical_coverage
        self.service = service
        self.format = format_
        self.technical_source = technical_source
        self.tag_id = tag_id
        self.license = license
        self.publication_restriction = publication_restriction


class DatasetCreate(CreateDatasetValidationMixin, BaseModel):
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
    extra_field_values: List[ExtraFieldValueCreate] = Field(default_factory=list)
    publication_restriction: Optional[
        PublicationRestriction
    ] = PublicationRestriction.NO_RESTRICTION


class DatasetUpdate(UpdateDatasetValidationMixin, BaseModel):
    title: str
    description: str
    service: str
    geographical_coverage: str
    format_ids: List[int]
    technical_source: Optional[str] = Field(...)
    producer_email: Optional[EmailStr] = Field(...)
    contact_emails: List[EmailStr]
    update_frequency: Optional[UpdateFrequency] = Field(...)
    last_updated_at: Optional[dt.datetime] = Field(...)
    url: Optional[str] = Field(...)
    license: Optional[str] = Field(...)
    tag_ids: List[ID]
    extra_field_values: List[ExtraFieldValueCreate] = Field(default_factory=list)
    publication_restriction: Optional[PublicationRestriction] = Field(...)
