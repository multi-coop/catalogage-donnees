"""add-catalog

Revision ID: 4e40358ad25c
Revises: da164fd0fa6f
Create Date: 2022-07-19 15:03:34.512545

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4e40358ad25c"
down_revision = "da164fd0fa6f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "catalog",
        sa.Column("organization_siret", sa.CHAR(length=14), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["organization_siret"], ["organization.siret"]),
        sa.PrimaryKeyConstraint("organization_siret"),
    )


def downgrade():
    op.drop_table("catalog")
