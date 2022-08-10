"""add-user-role

Revision ID: 1cbaaf0d013b
Revises: 67a6c2bf0696
Create Date: 2022-04-07 15:20:46.698308

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1cbaaf0d013b"
down_revision = "67a6c2bf0696"
branch_labels = None
depends_on = None

user_role_enum = sa.Enum("USER", "ADMIN", name="user_role_enum")


def upgrade():
    user_role_enum.create(op.get_bind())
    op.add_column(
        "user",
        sa.Column("role", user_role_enum, server_default="USER", nullable=False),
    )
    op.alter_column("user", "role", server_default=None)


def downgrade():
    op.drop_column("user", "role")
    user_role_enum.drop(op.get_bind())
