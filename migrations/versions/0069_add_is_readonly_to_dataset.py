"""Add is_readonly to dataset

Revision ID: 0069
Revises: 0068
Create Date: 2026-06-23 12:28:03.511624

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0069"
down_revision = "0068"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("is_readonly", sa.Boolean(), server_default="1"))


def downgrade():
    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.drop_column("is_readonly")
