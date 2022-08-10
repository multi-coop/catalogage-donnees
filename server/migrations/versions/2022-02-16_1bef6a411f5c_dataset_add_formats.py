"""dataset-add-formats

Revision ID: 1bef6a411f5c
Revises: 7b3e0dc2a28e
Create Date: 2022-02-16 15:31:29.685734

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1bef6a411f5c"
down_revision = "7b3e0dc2a28e"
branch_labels = None
depends_on = None

dataformat_values = (
    "FILE_TABULAR",
    "FILE_GIS",
    "API",
    "DATABASE",
    "WEBSITE",
    "OTHER",
)

dataformat_enum = sa.Enum(*dataformat_values, name="dataformat_enum")


def upgrade():
    dataformat_table = op.create_table(
        "dataformat",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", dataformat_enum, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "dataset_dataformat",
        sa.Column("dataformat_id", sa.Integer(), nullable=False),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataformat_id"],
            ["dataformat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("dataformat_id", "dataset_id"),
    )

    # Add one row per data format
    op.bulk_insert(dataformat_table, [{"name": value} for value in dataformat_values])


def downgrade():
    op.drop_table("dataset_dataformat")
    op.drop_table("dataformat")
