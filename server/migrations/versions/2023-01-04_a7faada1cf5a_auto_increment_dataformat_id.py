"""auto_increment_dataformat_id

Revision ID: a7faada1cf5a
Revises: 5245c239bca5
Create Date: 2023-01-04 16:40:58.719591

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a7faada1cf5a"
down_revision = "5245c239bca5"
branch_labels = None
depends_on = None


def upgrade():
    # Create the sequence
    op.execute("CREATE SEQUENCE table_name_id_seq START WITH 10")

    # Set the "id" column to auto-increment
    op.alter_column(
        "dataformat",
        "id",
        existing_type=sa.Integer,
        primary_key=True,
        server_default=sa.text("nextval('table_name_id_seq'::regclass)"),
    )


def downgrade():
    # Set the "id" column to not auto-increment
    op.alter_column(
        "dataformat",
        "id",
        existing_type=sa.Integer,
        primary_key=True,
        server_default=None,
    )

    # Drop the sequence
    op.execute("DROP SEQUENCE table_name_id_seq")
