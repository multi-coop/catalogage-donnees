"""add-extra-fields

Revision ID: 21a0f4491f8d
Revises: 3928481ec7d2
Create Date: 2022-08-09 15:55:39.537207

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "21a0f4491f8d"
down_revision = "3928481ec7d2"
branch_labels = None
depends_on = None

extra_field_type_enum = sa.Enum("TEXT", "ENUM", "BOOL", name="extra_field_type_enum")


def upgrade():
    op.create_table(
        "extra_field",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_siret", sa.CHAR(length=14), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("hint_text", sa.String(), nullable=False),
        sa.Column("type", extra_field_type_enum, nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_siret"],
            ["catalog.organization_siret"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_extra_field_organization_siret",
        "extra_field",
        ["organization_siret"],
    )
    op.create_index(
        "ix_extra_field_unique_organization_siret_name",
        "extra_field",
        ["organization_siret", "name"],
        unique=True,
    )

    op.create_table(
        "extra_field_value",
        sa.Column("dataset_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("extra_field_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("value", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(
            ["dataset_id"],
            ["dataset.id"],
        ),
        sa.ForeignKeyConstraint(
            ["extra_field_id"],
            ["extra_field.id"],
        ),
        sa.PrimaryKeyConstraint("dataset_id", "extra_field_id"),
    )


def downgrade():
    op.drop_table("extra_field_value")
    op.drop_table("extra_field")
    extra_field_type_enum.drop(op.get_bind())
