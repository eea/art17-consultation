"""empty message

Revision ID: 778050f6c279
Revises: 0047
Create Date: 2024-05-09 14:04:19.506871

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0048"
down_revision = "0047"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "registered_users",
        "account_date",
        existing_type=sa.String(length=16),
        type_=sa.String(length=100),
    )


def downgrade():
    op.alter_column(
        "registered_users",
        "account_date",
        existing_type=sa.String(length=100),
        type_=sa.String(length=16),
    )
