"""update-dataset-title-description

Revision ID: f050fa78b42c
Revises: d24cec0c6ddd
Create Date: 2022-01-17 11:45:52.382228

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f050fa78b42c"
down_revision = "d24cec0c6ddd"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("dataset", "name", new_column_name="title")
    op.add_column("dataset", sa.Column("description", sa.String(), nullable=False))


def downgrade():
    op.alter_column("dataset", "title", new_column_name="name")
    op.drop_column("dataset", "description")
