"""user-add-password-token

Revision ID: 30474ebed7a2
Revises: cc869b534916
Create Date: 2022-03-01 16:24:53.881795

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "30474ebed7a2"
down_revision = "cc869b534916"
branch_labels = None
depends_on = None

API_TOKEN_LENGTH = 64


def upgrade():
    # Hash for "changeme"
    default_password_hash = "$argon2id$v=19$m=65536,t=3,p=4$2/LvwQp6Bm5bbRvnFNTivQ$GtK4plgCCfrwVnSH7PdAJni9KeQ1qr0tmM88v2deo9A"  # noqa: E501

    op.add_column(
        "user",
        sa.Column(
            "password_hash",
            sa.String(),
            nullable=False,
            server_default=default_password_hash,
        ),
    )

    op.alter_column("user", "password_hash", server_default=None)

    # Sample result for `secrets.token_hex(API_TOKEN_LENGTH // 2)`
    default_api_token = (
        "9cd0c1b46e11cef4c713815690e845186385faf0aaaf9495bd47027ecb378f79"  # noqa: E501
    )

    op.add_column(
        "user",
        sa.Column(
            "api_token",
            sa.String(API_TOKEN_LENGTH),
            nullable=False,
            server_default=default_api_token,
        ),
    )

    op.alter_column("user", "api_token", server_default=None)


def downgrade():
    op.drop_column("user", "api_token")
    op.drop_column("user", "password_hash")
