"""split-account-password-user

Revision ID: 17a9b8d2f84e
Revises: f2ef4eef61e3
Create Date: 2022-08-02 11:07:59.669511
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "17a9b8d2f84e"
down_revision = "f2ef4eef61e3"
branch_labels = None
depends_on = None


def upgrade():
    # Users become accounts.
    op.rename_table("user", "account")
    op.execute("ALTER INDEX user_pkey RENAME TO account_pkey;")
    op.execute("ALTER INDEX ix_user_email RENAME TO ix_account_email;")
    op.execute(
        """
        ALTER TABLE account
        RENAME CONSTRAINT user_organization_siret_fkey
        TO account_organization_siret_fkey;
        """
    )

    op.create_table(
        "password_user",
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["account.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("account_id"),
    )

    # Create password users from existing accounts.
    op.execute(
        """
        INSERT INTO password_user (account_id, password_hash)
        SELECT account.id, account.password_hash FROM account;
        """
    )

    op.drop_column("account", "password_hash")


def downgrade():
    # Move password_hash back to accounts.
    op.add_column(
        "account",
        sa.Column("password_hash", sa.String()),
    )
    op.execute(
        """
        UPDATE account
        SET password_hash = pu.password_hash
        FROM password_user AS pu
        JOIN account AS acc ON pu.account_id = acc.id;
        """
    )
    op.alter_column("account", "password_hash", nullable=False)

    op.drop_table("password_user")

    # Accounts become users.
    op.execute("ALTER INDEX account_pkey RENAME TO user_pkey;")
    op.execute("ALTER INDEX ix_account_email RENAME TO ix_user_email;")
    op.execute(
        """
        ALTER TABLE account
        RENAME CONSTRAINT account_organization_siret_fkey
        TO user_organization_siret_fkey;
        """
    )
    op.rename_table("account", "user")
