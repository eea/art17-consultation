"""Add envelope text to etc data species regions

Revision ID: 0064
Revises: 0063
Create Date: 2026-03-27 12:11:10.531725

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0064'
down_revision = '0063'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_data_species_regions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('envelope_text', sa.Text(), nullable=True))

def downgrade():
    with op.batch_alter_table('etc_data_species_regions', schema=None) as batch_op:
        batch_op.drop_column('envelope_text')
