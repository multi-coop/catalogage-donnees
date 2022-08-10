"""add-dataset-published-url

Revision ID: 531a8496be5e
Revises: 012e4606ddc1
Create Date: 2022-04-25 16:36:43.984156

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "531a8496be5e"
down_revision = "012e4606ddc1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("dataset", sa.Column("published_url", sa.String(), nullable=True))


def downgrade():
    op.drop_column("dataset", "published_url")
