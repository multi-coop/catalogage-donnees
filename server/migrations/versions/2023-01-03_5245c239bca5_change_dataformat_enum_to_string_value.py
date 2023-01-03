"""change_dataformat_enum_to_string_value

Revision ID: 5245c239bca5
Revises: a6fd9d9cdb24
Create Date: 2023-01-03 16:47:05.844552

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5245c239bca5"
down_revision = "a6fd9d9cdb24"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("dataformat", "name", type_=sa.VARCHAR())


def downgrade():
    dataformat_values = (
        "FILE_TABULAR",
        "FILE_GIS",
        "API",
        "DATABASE",
        "WEBSITE",
        "OTHER",
    )

    dataformat_enum = sa.Enum(*dataformat_values, name="dataformat_enum")
    op.add_column("data_format", "name", type=dataformat_enum)
