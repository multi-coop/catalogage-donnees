"""add-datapass-user

Revision ID: 3928481ec7d2
Revises: 17a9b8d2f84e
Create Date: 2022-08-03 13:31:46.358473

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "3928481ec7d2"
down_revision = "17a9b8d2f84e"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "datapass_user",
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("account_id"),
    )


def downgrade():
    op.drop_table("datapass_user")
