from typing import TYPE_CHECKING, List

from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table
from sqlalchemy.orm import relationship

from ..database import Base, mapper_registry

if TYPE_CHECKING:  # pragma: no cover
    from ..datasets.models import DatasetModel

# Association table
# See: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
dataset_dataformat = Table(
    "dataset_dataformat",
    mapper_registry.metadata,
    Column("dataset_id", ForeignKey("dataset.id"), primary_key=True, index=True),
    Column("dataformat_id", ForeignKey("dataformat.id"), primary_key=True),
)

TABLE_ID: Sequence = Sequence("table_name_id_seq", start=10)


class DataFormatModel(Base):
    __tablename__ = "dataformat"

    id = Column(
        Integer, TABLE_ID, primary_key=True, server_default=TABLE_ID.next_value()
    )
    name = Column(String, nullable=False, unique=True)

    datasets: List["DatasetModel"] = relationship(
        "DatasetModel",
        back_populates="formats",
        secondary=dataset_dataformat,
    )
