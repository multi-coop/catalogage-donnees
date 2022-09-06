import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import CHAR, Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from server.domain.common.types import ID
from server.domain.organizations.types import Siret

from ..database import Base

if TYPE_CHECKING:  # pragma: no cover
    from ..catalogs.models import CatalogModel
    from ..datasets.models import DatasetModel


class CatalogRecordModel(Base):
    __tablename__ = "catalog_record"

    id: ID = Column(UUID(as_uuid=True), primary_key=True)
    created_at: dt.datetime = Column(
        DateTime(timezone=True), server_default=func.clock_timestamp(), nullable=False
    )
    organization_siret: Siret = Column(
        CHAR(14),
        ForeignKey("catalog.organization_siret"),
        nullable=False,
    )

    catalog: "CatalogModel" = relationship(
        "CatalogModel",
        back_populates="catalog_records",
    )

    dataset: "DatasetModel" = relationship(
        "DatasetModel",
        back_populates="catalog_record",
    )
