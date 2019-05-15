revision = '50974899f7aa'
down_revision = '1bcf826b011a'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment', sa.Column('method_area',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions', sa.Column('method_area',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_automatic_assessment', sa.Column('population_method',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions', sa.Column('population_method',
                  sa.String(length=50), nullable=True))
    op.drop_column('habitattypes_manual_assessment', 'type_estimate_area')
    op.drop_column('species_manual_assessment', 'population_size_type_estimate')

def downgrade():
    op.add_column('species_manual_assessment', 
                  sa.Column('population_size_type_estimate', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('type_estimate_area', mysql.VARCHAR(length=50), nullable=True))
    op.drop_column('etc_data_species_regions', 'population_method')
    op.drop_column('etc_data_species_automatic_assessment', 'population_method')
    op.drop_column('etc_data_habitattype_regions', 'method_area')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'method_area')
