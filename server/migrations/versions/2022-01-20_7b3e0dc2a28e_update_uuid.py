"""update-uuid

Revision ID: 7b3e0dc2a28e
Revises: d24cec0c6ddd
Create Date: 2022-01-20 16:01:04.826820

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7b3e0dc2a28e"
down_revision = "f050fa78b42c"
branch_labels = None
depends_on = None


def upgrade():
    # Allows using the PostgreSQL UUID type and
    # uuid_generate_v4() (UUID4 random generator).
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # This index was redundant with the one on the primary key (user_pkey),
    # so we drop it here.
    op.drop_index(op.f("ix_user_id"), table_name="user")

    # We change the type of the id column from SEQUENTIAL to UUID.
    # We can fill the new UUIDs with uuid_generate_v4(), but we need to drop
    # the column's default (i.e. next integer in the sequence) first, otherwise
    # the ALTER COLUMN would try to apply this default integer to the new UUID column,
    # resulting in an error.
    # There's no SQLAlchemy API for this, so we use raw SQL.
    op.execute('ALTER TABLE "user" ALTER COLUMN id DROP DEFAULT;')
    op.alter_column(
        "user",
        "id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="(uuid_generate_v4())",
    )
    # Now we can set the default generated UUID for future additional rows.
    op.execute('ALTER TABLE "user" ALTER COLUMN id SET DEFAULT uuid_generate_v4();')

    # Pretty much the same thing for datasets.
    op.drop_index(op.f("ix_dataset_id"), table_name="dataset")
    op.execute('ALTER TABLE "dataset" ALTER COLUMN id DROP DEFAULT;')
    op.alter_column(
        "dataset",
        "id",
        type_=postgresql.UUID(as_uuid=True),
        postgresql_using="(uuid_generate_v4())",
    )
    op.execute('ALTER TABLE "dataset" ALTER COLUMN id SET DEFAULT uuid_generate_v4();')


def downgrade():
    raise NotImplementedError
