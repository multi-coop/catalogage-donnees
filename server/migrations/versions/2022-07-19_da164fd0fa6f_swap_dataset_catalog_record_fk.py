"""swap-dataset-catalog_record-fk

Revision ID: da164fd0fa6f
Revises: d9ea6ea6708f
Create Date: 2022-07-19 16:25:43.333190

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "da164fd0fa6f"
down_revision = "d9ea6ea6708f"
branch_labels = None
depends_on = None


def upgrade():
    # Drop old FK constraint.
    op.drop_constraint(
        "catalog_record_dataset_id_fkey",
        "catalog_record",
        type_="foreignkey",
    )

    # Add and fill new FK column and constraint.
    op.add_column(
        "dataset",
        sa.Column("catalog_record_id", postgresql.UUID(as_uuid=True)),
    )
    op.execute(
        "UPDATE dataset SET catalog_record_id = catalog_record.id "
        "FROM dataset AS d JOIN catalog_record ON d.id = catalog_record.dataset_id "
        "WHERE d.id = dataset.id;"
    )
    op.alter_column("dataset", "catalog_record_id", nullable=False)
    op.create_foreign_key(
        "dataset_catalog_record_id_fkey",
        "dataset",
        "catalog_record",
        ["catalog_record_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Drop old FK column.
    op.drop_column("catalog_record", "dataset_id")


def downgrade():
    # Drop new FK constraint.
    op.drop_constraint("dataset_catalog_record_id_fkey", "dataset", type_="foreignkey")

    # Bring back and fill old FK column and constraint.
    op.add_column(
        "catalog_record",
        sa.Column("dataset_id", postgresql.UUID(), autoincrement=False, nullable=True),
    )
    op.execute(
        "UPDATE catalog_record SET dataset_id = dataset.id "
        "FROM catalog_record AS cr JOIN dataset ON cr.id = dataset.catalog_record_id "
        "WHERE cr.id = catalog_record.id;"
    )
    op.create_foreign_key(
        "catalog_record_dataset_id_fkey",
        "catalog_record",
        "dataset",
        ["dataset_id"],
        ["id"],
    )

    # Drop new FK column.
    op.drop_column("dataset", "catalog_record_id")
