revision = '26182e07944b'
down_revision = '135e379e27ba'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_unit', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_unit', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('backcasted_2007', sa.String(length=3), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('backcasted_2007', sa.String(length=3), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_unit', sa.String(length=20), nullable=True))

def downgrade():
    op.drop_column('species_manual_assessment', 'population_unit')
    op.drop_column('species_manual_assessment', 'backcasted_2007')
    op.drop_column('habitattypes_manual_assessment', 'backcasted_2007')
    op.drop_column('etc_data_species_regions', 'population_unit')
    op.drop_column('etc_data_species_automatic_assessment', 'population_unit')
