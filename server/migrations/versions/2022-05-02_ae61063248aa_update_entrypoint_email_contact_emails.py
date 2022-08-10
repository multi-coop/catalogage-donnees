"""update-entrypoint_email-contact_emails

Revision ID: ae61063248aa
Revises: 531a8496be5e
Create Date: 2022-05-02 15:02:05.907850

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "ae61063248aa"
down_revision = "531a8496be5e"
branch_labels = None
depends_on = None


def upgrade():
    # Heuristic: add initial entrypoint_email to contact_emails to ensure it contains
    # at least one item.
    op.execute(
        """
        UPDATE dataset
        SET contact_emails = array_prepend(
            entrypoint_email,
            coalesce(contact_emails, '{}')
        );
        """
    )

    op.alter_column("dataset", "contact_emails", nullable=False)
    op.alter_column(
        "dataset", "entrypoint_email", new_column_name="producer_email", nullable=True
    )


def downgrade():
    # Heuristic: when rolling back, assume first contact email refers to producer.
    op.execute("UPDATE dataset SET producer_email = contact_emails[1];")
    op.execute("UPDATE dataset SET contact_emails = contact_emails[2:];")

    op.alter_column(
        "dataset", "producer_email", new_column_name="entrypoint_email", nullable=False
    )
    op.alter_column("dataset", "contact_emails", nullable=True)
