"""add-catalog-record

Revision ID: 012e4606ddc1
Revises: f92d0ee57d88
Create Date: 2022-04-20 17:28:46.738810

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "012e4606ddc1"
down_revision = "f92d0ee57d88"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "catalog_record",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create one catalog record per existing dataset, transferring created_at
    op.execute(
        """
        INSERT INTO catalog_record (dataset_id, created_at)
        SELECT id, created_at FROM dataset;
        """
    )

    op.drop_column("dataset", "created_at")


def downgrade():
    op.add_column(
        "dataset",
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            autoincrement=False,
            nullable=False,
        ),
    )

    op.drop_table("catalog_record")
