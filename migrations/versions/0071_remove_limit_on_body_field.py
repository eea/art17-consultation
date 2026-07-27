"""Remove limit on body fields from wiki

Revision ID: 0071
Revises: 0070
Create Date: 2026-07-10 07:24:40.794555

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0071"
down_revision = "0070"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("wiki_changes", schema=None) as batch_op:
        batch_op.alter_column(
            "body",
            existing_type=sa.VARCHAR(length=6000),
            type_=sa.Text(),
            existing_nullable=True,
        )

    with op.batch_alter_table("wiki_trail_changes", schema=None) as batch_op:
        batch_op.alter_column(
            "body",
            existing_type=sa.VARCHAR(length=6000),
            type_=sa.Text(),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("wiki_trail_changes", schema=None) as batch_op:
        batch_op.alter_column(
            "body",
            existing_type=sa.Text(),
            type_=sa.VARCHAR(length=6000),
            existing_nullable=True,
        )

    with op.batch_alter_table("wiki_changes", schema=None) as batch_op:
        batch_op.alter_column(
            "body",
            existing_type=sa.Text(),
            type_=sa.VARCHAR(length=6000),
            existing_nullable=True,
        )
