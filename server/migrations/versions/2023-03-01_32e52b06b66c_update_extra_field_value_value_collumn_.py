"""update_extra_field_value_value_collumn_from_jsonb_to_string

Revision ID: 32e52b06b66c
Revises: a7faada1cf5a
Create Date: 2023-03-01 08:35:40.288340

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = "32e52b06b66c"
down_revision = "a7faada1cf5a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("extra_field_value", "value", type_=sa.VARCHAR())
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("extra_field_value", "value", type_=JSONB())
    # ### end Alembic commands ###