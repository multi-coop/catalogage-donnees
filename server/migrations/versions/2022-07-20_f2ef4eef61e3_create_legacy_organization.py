"""create-legacy-organization

Revision ID: f2ef4eef61e3
Revises: 4e40358ad25c
Create Date: 2022-07-20 16:43:10.140605

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f2ef4eef61e3"
down_revision = "4e40358ad25c"
branch_labels = None
depends_on = None


def upgrade():
    # Create initial organization.
    op.execute(
        "INSERT INTO organization (siret, name) "
        "VALUES ('00000000000000', 'Organisation par défaut');"
    )

    # Add all users to it.
    op.add_column("user", sa.Column("organization_siret", sa.CHAR(14)))
    op.execute("UPDATE \"user\" SET organization_siret = '00000000000000';")
    op.alter_column("user", "organization_siret", nullable=False)
    op.create_foreign_key(
        "user_organization_siret_fkey",
        "user",
        "organization",
        ["organization_siret"],
        ["siret"],
    )

    # Create its catalog.
    op.execute("INSERT INTO catalog (organization_siret) VALUES ('00000000000000');")

    # Add all catalog records to it.
    op.add_column("catalog_record", sa.Column("organization_siret", sa.CHAR(14)))
    op.execute("UPDATE catalog_record SET organization_siret = '00000000000000';")
    op.alter_column("catalog_record", "organization_siret", nullable=False)
    op.create_foreign_key(
        "catalog_record_organization_siret_fkey",
        "catalog_record",
        "catalog",
        ["organization_siret"],
        ["organization_siret"],
    )


def downgrade():
    # Drop link between users and legacy organization.
    op.drop_constraint("user_organization_siret_fkey", "user", type_="foreignkey")
    op.drop_column("user", "organization_siret")

    # Drop link between catalog records and legacy organization.
    op.drop_constraint(
        "catalog_record_organization_siret_fkey", "catalog_record", type_="foreignkey"
    )
    op.drop_column("catalog_record", "organization_siret")

    # Delete legacy catalog, then legacy organization.
    op.execute("DELETE FROM catalog WHERE organization_siret = '00000000000000';")
    op.execute("DELETE FROM organization WHERE siret = '00000000000000';")
