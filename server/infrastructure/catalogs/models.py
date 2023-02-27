import datetime as dt
from typing import TYPE_CHECKING, List

from sqlalchemy import CHAR, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:  # pragma: no cover
    from server.infrastructure.extra_fields.models import ExtraFieldModel

    from ..catalog_records.models import CatalogRecordModel
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
