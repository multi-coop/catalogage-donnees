import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base, mapper_registry

if TYPE_CHECKING:  # pragma: no cover
    from ..datasets.models import DatasetModel


dataset_tag = Table(
    "dataset_tag",
    mapper_registry.metadata,
    Column("dataset_id", ForeignKey("dataset.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class TagModel(Base):
    __tablename__ = "tag"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)

    datasets: List["DatasetModel"] = relationship(
        "DatasetModel", back_populates="tags", secondary=dataset_tag
    )
