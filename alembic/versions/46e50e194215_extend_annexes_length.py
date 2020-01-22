revision = '46e50e194215'
down_revision = '3f68d0711600'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('etc_data_species_regions', 'annex_II',
    existing_type=sa.String(length=2), type_=sa.String(length=5))
    op.alter_column('etc_data_species_regions', 'annex_IV',
    existing_type=sa.String(length=2), type_=sa.String(length=5))
    op.alter_column('etc_data_species_regions', 'annex_V',
    existing_type=sa.String(length=2), type_=sa.String(length=5))

def downgrade():
    op.alter_column('etc_data_species_regions', 'annex_V',
    existing_type=sa.String(length=5), type_=sa.String(length=2))
    op.alter_column('etc_data_species_regions', 'annex_IV',
    existing_type=sa.String(length=5), type_=sa.String(length=2))
    op.alter_column('etc_data_species_regions', 'annex_II',
    existing_type=sa.String(length=5), type_=sa.String(length=2))