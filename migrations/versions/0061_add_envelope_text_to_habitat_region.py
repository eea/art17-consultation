"""Add envelope_text to habitat region

Revision ID: 0061
Revises: 0060
Create Date: 2026-03-05 13:12:20.942134

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0061"
down_revision = "0060"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.add_column(sa.Column("envelope_text", sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.drop_column("envelope_text")
