import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, Computed, DateTime, Enum, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, relationship

from server.domain.datasets.entities import PublicationRestriction, UpdateFrequency
from server.infrastructure.extra_fields.models import ExtraFieldValueModel

from ..database import Base
from ..dataformats.models import DataFormatModel, dataset_dataformat
from ..tags.models import TagModel, dataset_tag

if TYPE_CHECKING:  # pragma: no cover
    from ..catalog_records.models import CatalogRecordModel


class DatasetModel(Base):
    __tablename__ = "dataset"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)

    catalog_record_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("catalog_record.id", ondelete="CASCADE"),
        nullable=False,
    )
    catalog_record: "CatalogRecordModel" = relationship(
        "CatalogRecordModel",
        back_populates="dataset",
        cascade="delete",
        uselist=False,
    )

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    service = Column(String, nullable=False)
    geographical_coverage = Column(String, nullable=False)
    formats: List[DataFormatModel] = relationship(
        "DataFormatModel",
        back_populates="datasets",
        secondary=dataset_dataformat,
    )
    technical_source = Column(String)
    producer_email = Column(String, nullable=True)
    contact_emails = Column(ARRAY(String), server_default="{}", nullable=False)
    update_frequency = Column(Enum(UpdateFrequency, enum="update_frequency_enum"))
    publication_restriction = Column(
        Enum(PublicationRestriction, enum="publication_restriction_enum")
    )
    last_updated_at = Column(DateTime(timezone=True))
    url = Column(String)
    license = Column(String)
    tags: List["TagModel"] = relationship(
        "TagModel", back_populates="datasets", secondary=dataset_tag
    )
    extra_field_values: List["ExtraFieldValueModel"] = relationship(
        "ExtraFieldValueModel", cascade="all, delete-orphan", back_populates="dataset"
    )

    search_tsv: Mapped[str] = Column(
        TSVECTOR,
        Computed("to_tsvector('french', title || ' ' || description)", persisted=True),
    )

    __table_args__ = (
        Index(
            "ix_dataset_search_tsv",
            search_tsv,
            postgresql_using="GIN",
        ),
    )
