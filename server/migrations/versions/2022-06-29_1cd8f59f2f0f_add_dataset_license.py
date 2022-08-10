"""add-dataset-license

Revision ID: 1cd8f59f2f0f
Revises: b3dac4035ce9
Create Date: 2022-06-29 16:09:21.170267

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1cd8f59f2f0f"
down_revision = "b3dac4035ce9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("dataset", sa.Column("license", sa.String(), nullable=True))


def downgrade():
    op.drop_column("dataset", "license")
