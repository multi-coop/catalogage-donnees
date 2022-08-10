"""dataset_add_created_at

Revision ID: 26e723d032b1
Revises: 30474ebed7a2
Create Date: 2022-03-16 15:50:00.805743

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "26e723d032b1"
down_revision = "30474ebed7a2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "dataset",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("clock_timestamp()"),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("dataset", "created_at")
