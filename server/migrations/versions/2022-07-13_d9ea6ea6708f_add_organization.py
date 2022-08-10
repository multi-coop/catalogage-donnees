"""add-organization

Revision ID: d9ea6ea6708f
Revises: 663792a4c86c
Create Date: 2022-07-13 14:39:44.348452

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d9ea6ea6708f"
down_revision = "663792a4c86c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "organization",
        sa.Column("siret", sa.CHAR(length=14), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("siret"),
    )


def downgrade():
    op.drop_table("organization")
