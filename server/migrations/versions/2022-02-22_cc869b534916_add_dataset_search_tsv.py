"""add-dataset-search-tsv

Revision ID: cc869b534916
Revises: 1bef6a411f5c
Create Date: 2022-02-22 19:11:56.402112

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cc869b534916"
down_revision = "1bef6a411f5c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "dataset",
        sa.Column(
            "search_tsv",
            postgresql.TSVECTOR(),
            sa.Computed(
                "to_tsvector('french', title || ' ' || description)", persisted=True
            ),
            nullable=True,
        ),
    )
    op.create_index(
        "ix_dataset_search_tsv",
        "dataset",
        ["search_tsv"],
        unique=False,
        postgresql_using="GIN",
    )


def downgrade():
    op.drop_index("ix_dataset_search_tsv", table_name="dataset", postgresql_using="GIN")
    op.drop_column("dataset", "search_tsv")
