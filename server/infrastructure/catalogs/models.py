import datetime as dt
from typing import TYPE_CHECKING, Any, List

from sqlalchemy import CHAR, Column, DateTime, Enum, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from server.domain.catalogs.entities import ExtraFieldType
from server.domain.common.types import ID
from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:  # pragma: no cover
    from ..catalog_records.models import CatalogRecordModel
    from ..datasets.models import DatasetModel
    from ..organizations.models import OrganizationModel


class CatalogModel(Base):
    __tablename__ = "catalog"

    organization_siret: Siret = Column(
        CHAR(14),
        ForeignKey("organization.siret"),
        primary_key=True,
    )
    organization: "OrganizationModel" = relationship(
        "OrganizationModel",
        back_populates="catalog",
    )
    created_at: dt.datetime = Column(
        DateTime(timezone=True),
        server_default=func.clock_timestamp(),
        nullable=False,
    )

    catalog_records: List["CatalogRecordModel"] = relationship(
        "CatalogRecordModel",
        back_populates="catalog",
    )
    extra_fields: List["ExtraFieldModel"] = relationship(
        "ExtraFieldModel",
        back_populates="catalog",
    )


class ExtraFieldModel(Base):
    __tablename__ = "extra_field"

    id: ID = Column(UUID(as_uuid=True), primary_key=True)
    organization_siret: Siret = Column(
        CHAR(14),
        ForeignKey("catalog.organization_siret"),
        nullable=False,
        index=True,
    )
    name = Column(String(), nullable=False)
    title = Column(String(), nullable=False)
    hint_text = Column(String(), nullable=False)
    type: ExtraFieldType = Column(
        Enum(ExtraFieldType, name="extra_field_type_enum"), nullable=False
    )
    data: dict = Column(JSONB(), nullable=False)
    catalog: "CatalogModel" = relationship(
        "CatalogModel", back_populates="extra_fields"
    )
    values: List["ExtraFieldValueModel"] = relationship(
        "ExtraFieldValueModel", back_populates="extra_field"
    )

    __table_args__ = (
        Index(
            "ix_extra_field_unique_organization_siret_name",
            organization_siret,
            name,
            unique=True,
        ),
    )


class ExtraFieldValueModel(Base):
    __tablename__ = "extra_field_value"

    dataset_id: ID = Column(
        UUID(as_uuid=True), ForeignKey("dataset.id"), primary_key=True
    )
    dataset: "DatasetModel" = relationship(
        "DatasetModel", back_populates="extra_field_values"
    )
    extra_field_id: ID = Column(
        UUID(as_uuid=True), ForeignKey("extra_field.id"), primary_key=True
    )
    extra_field: "ExtraFieldModel" = relationship(
        "ExtraFieldModel", back_populates="values"
    )
    value: Any = Column(JSONB(), nullable=False)
