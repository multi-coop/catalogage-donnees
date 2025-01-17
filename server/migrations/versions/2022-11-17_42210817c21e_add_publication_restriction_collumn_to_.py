"""add_publication_restriction_collumn_to_dataset

Revision ID: 42210817c21e
Revises: 0ae635406834
Create Date: 2022-11-17 15:17:54.689973

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "42210817c21e"
down_revision = "0ae635406834"
branch_labels = None
depends_on = None

publication_restriction_enum = sa.Enum(
    "LEGAL_RESTRICTION",
    "DRAFT",
    "NO_RESTRICTION",
    name="publication_restriction_enum",
)


def upgrade():

    publication_restriction_enum.create(op.get_bind())
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "dataset",
        sa.Column(
            "publication_restriction",
            publication_restriction_enum,
            nullable=False,
            server_default="NO_RESTRICTION",
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("dataset", "publication_restriction")
    # ### end Alembic commands ###
    publication_restriction_enum.drop(op.get_bind())
