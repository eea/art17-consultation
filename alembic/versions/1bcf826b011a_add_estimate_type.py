revision = '1bcf826b011a'
down_revision = '1ad00462f2d4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment', sa.Column('type_estimate_area', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions', sa.Column('type_estimate_area', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_automatic_assessment', sa.Column('population_size_type_estimate', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions', sa.Column('population_size_type_estimate', sa.String(length=50), nullable=True))
    op.add_column('habitattypes_manual_assessment', sa.Column('type_estimate_area', sa.String(length=50), nullable=True))
    op.add_column('species_manual_assessment', sa.Column('population_size_type_estimate', sa.String(length=50), nullable=True))

def downgrade():
    op.drop_column('species_manual_assessment', 'population_size_type_estimate')
    op.drop_column('habitattypes_manual_assessment', 'type_estimate_area')
    op.drop_column('etc_data_species_regions', 'population_size_type_estimate')
    op.drop_column('etc_data_species_automatic_assessment', 'population_size_type_estimate')
    op.drop_column('etc_data_habitattype_regions', 'type_estimate_area')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'type_estimate_area')
