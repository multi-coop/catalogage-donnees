"""change_dataformat_enum_to_string_value

Revision ID: 5245c239bca5
Revises: a6fd9d9cdb24
Create Date: 2023-01-03 16:47:05.844552

"""
# flake8: noqa

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "5245c239bca5"
down_revision = "a6fd9d9cdb24"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("dataformat", "name", type_=sa.VARCHAR())
    op.execute(
        "UPDATE dataformat SET name = 'Fichier tabulaire (XLS, XLSX, CSV, ...)' WHERE name = 'FILE_TABULAR'"
    )
    op.execute(
        "UPDATE dataformat SET name = 'Fichier SIG (Shapefile, ...)' WHERE name = 'FILE_GIS'"
    )
    op.execute("UPDATE dataformat SET name = 'Base de données' WHERE name = 'DATABASE'")
    op.execute(
        "UPDATE dataformat SET name = 'API (REST, GraphQL, ...)' WHERE name = 'API'"
    )
    op.execute("UPDATE dataformat SET name = 'Site web' WHERE name = 'WEBSITE'")
    op.execute("UPDATE dataformat SET name = 'Autre' WHERE name = 'OTHER'")


def downgrade():

    op.execute(
        "UPDATE dataformat SET name = 'FILE_TABULAR' WHERE name = 'Fichier tabulaire (XLS, XLSX, CSV, ...)'"
    )
    op.execute(
        "UPDATE dataformat SET name = 'FILE_GIS' WHERE name = 'Fichier SIG (Shapefile, ...)'"
    )
    op.execute(
        "UPDATE dataformat SET name = 'API' WHERE name = 'API (REST, GraphQL, ...)'"
    )
    op.execute("UPDATE dataformat SET name = 'DATABASE WHERE name = 'Base de données'")
    op.execute("UPDATE dataformat SET name = 'WEBSITE' WHERE name = 'Site web'")
    op.execute("UPDATE dataformat SET name = 'OTHER' WHERE name = 'Autre'")
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
