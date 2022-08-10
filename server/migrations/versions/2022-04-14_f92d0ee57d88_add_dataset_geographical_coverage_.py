"""add-dataset-geographical_coverage-technical_source

Revision ID: f92d0ee57d88
Revises: 6fd05f9d4158
Create Date: 2022-04-14 11:53:39.708368

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f92d0ee57d88"
down_revision = "6fd05f9d4158"
branch_labels = None
depends_on = None


geographical_coverage_enum = sa.Enum(
    "MUNICIPALITY",
    "EPCI",
    "DEPARTMENT",
    "REGION",
    "NATIONAL",
    "NATIONAL_FULL_TERRITORY",
    "EUROPE",
    "WORLD",
    name="geographical_coverage_enum",
)


def upgrade():
    geographical_coverage_enum.create(op.get_bind())
    op.add_column(
        "dataset",
        sa.Column(
            "geographical_coverage",
            geographical_coverage_enum,
            nullable=False,
            server_default="NATIONAL",
        ),
    )
    op.alter_column("dataset", "geographical_coverage", server_default=None)
    op.add_column("dataset", sa.Column("technical_source", sa.String(), nullable=True))


def downgrade():
    op.drop_column("dataset", "technical_source")
    op.drop_column("dataset", "geographical_coverage")
    geographical_coverage_enum.drop(op.get_bind())
