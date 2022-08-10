"""update-geographical-coverage-string

Revision ID: 663792a4c86c
Revises: 1cd8f59f2f0f
Create Date: 2022-07-11 12:21:40.319045

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "663792a4c86c"
down_revision = "1cd8f59f2f0f"
branch_labels = None
depends_on = None

geographical_coverage_enum = sa.Enum(
    "MUNICIPALITY",
    "EPCI",
    "DEPARTMENT",
    "REGION",
    "NATIONAL",
    "NATIONAL_FULL_TERRITORY",
    "EUROPE",
    "WORLD",
    name="geographical_coverage_enum",
)


def upgrade():
    op.alter_column(
        "dataset",
        "geographical_coverage",
        type_=sa.String(),
        server_default=None,
    )

    # Convert enum values to human-readable labels.
    op.execute(
        """
        UPDATE dataset
        SET geographical_coverage =
            CASE
                WHEN geographical_coverage = 'MUNICIPALITY' THEN 'Communale'
                WHEN geographical_coverage = 'EPCI' THEN 'EPCI'
                WHEN geographical_coverage = 'DEPARTMENT' THEN 'Départementale'
                WHEN geographical_coverage = 'REGION' THEN 'Régionale'
                WHEN geographical_coverage= 'NATIONAL' THEN 'France'
                WHEN geographical_coverage= 'NATIONAL_FULL_TERRITORY' THEN 'France entière'
                WHEN geographical_coverage= 'EUROPE' THEN 'Europe'
                WHEN geographical_coverage= 'WORLD' THEN 'Monde'
            END;
        """  # noqa: E501
    )

    geographical_coverage_enum.drop(op.get_bind())


def downgrade():
    geographical_coverage_enum.create(op.get_bind())

    # Coerce existing values to enum values, or use a default.
    op.execute(
        """
        UPDATE dataset
        SET geographical_coverage =
            CASE
                WHEN geographical_coverage = 'Communale' THEN 'MUNICIPALITY'
                WHEN geographical_coverage = 'EPCI' THEN 'EPCI'
                WHEN geographical_coverage = 'Départementale' THEN 'DEPARTEMENT'
                WHEN geographical_coverage = 'Régionale' THEN 'REGION'
                WHEN geographical_coverage = 'France' THEN 'NATIONAL'
                WHEN geographical_coverage = 'France entière' THEN 'NATIONAL_FULL_TERRITORY'
                WHEN geographical_coverage = 'Europe' THEN 'EUROPE'
                WHEN geographical_coverage = 'Monde' THEN 'WORLD'
                ELSE 'NATIONAL'
            END;
        """  # noqa: E501
    )

    op.alter_column(
        "dataset",
        "geographical_coverage",
        type_=geographical_coverage_enum,
        postgresql_using="geographical_coverage::geographical_coverage_enum",
    )
