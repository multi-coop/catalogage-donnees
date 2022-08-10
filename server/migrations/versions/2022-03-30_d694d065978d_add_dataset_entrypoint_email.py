"""add-dataset-entrypoint-email

Revision ID: d694d065978d
Revises: 26e723d032b1
Create Date: 2022-03-30 14:50:05.651183

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d694d065978d"
down_revision = "26e723d032b1"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "dataset",
        sa.Column(
            "entrypoint_email",
            sa.String(),
            server_default="service@mydomain.org",
            nullable=False,
        ),
    )
    op.alter_column("dataset", "entrypoint_email", server_default=None)


def downgrade():
    op.drop_column("dataset", "entrypoint_email")
