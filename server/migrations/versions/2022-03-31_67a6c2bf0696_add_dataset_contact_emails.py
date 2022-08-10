"""add-dataset-contact-emails

Revision ID: 67a6c2bf0696
Revises: d694d065978d
Create Date: 2022-03-31 10:16:41.995848

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "67a6c2bf0696"
down_revision = "d694d065978d"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "dataset",
        sa.Column(
            "contact_emails",
            postgresql.ARRAY(sa.String()),
            server_default="{}",
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("dataset", "contact_emails")
