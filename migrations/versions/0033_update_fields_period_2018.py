revision = '0033'
down_revision = '0032'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('coverage_surface_area_max', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('coverage_surface_area_min', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('percentage_assessment_trend_unfavourable', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('percentage_coverage_trend', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('percentage_hab_condition_trend', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('percentage_range_trend', sa.String(length=100), nullable=True))
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_surface_area_min_max')
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('percentage_assessment_trend_unfavourable', sa.String(length=100), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('percentage_population_trend', sa.String(length=100), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('percentage_range_trend', sa.String(length=100), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_maximum_size', sa.String(length=100), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_minimum_size', sa.String(length=100), nullable=True))
    op.drop_column('etc_data_species_automatic_assessment', 'population_size_min_max')
    op.add_column('habitattypes_manual_assessment', 
                  sa.Column('coverage_surface_area_max', sa.String(length=23), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('coverage_surface_area_min', sa.String(length=23), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_maximum_size', sa.String(length=23), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_minimum_size', sa.String(length=23), nullable=True))
    op.add_column('etc_data_habitattype_regions', sa.Column('coverage_etc', 
                  sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions', sa.Column('percentage_hab_condition_good', 
                  sa.Float(asdecimal=True), nullable=True))


def downgrade():
    op.drop_column('etc_data_habitattype_regions', 'coverage_etc')
    op.drop_column('etc_data_habitattype_regions', 'percentage_hab_condition_good')
    op.drop_column('species_manual_assessment', 'population_minimum_size')
    op.drop_column('species_manual_assessment', 'population_maximum_size')
    op.drop_column('habitattypes_manual_assessment', 'coverage_surface_area_min')
    op.drop_column('habitattypes_manual_assessment', 'coverage_surface_area_max')
    op.add_column('etc_data_species_automatic_assessment', sa.Column('population_size_min_max', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('etc_data_species_automatic_assessment', 'population_minimum_size')
    op.drop_column('etc_data_species_automatic_assessment', 'population_maximum_size')
    op.drop_column('etc_data_species_automatic_assessment', 'percentage_range_trend')
    op.drop_column('etc_data_species_automatic_assessment', 'percentage_population_trend')
    op.drop_column('etc_data_species_automatic_assessment', 'percentage_assessment_trend_unfavourable')
    op.add_column('etc_data_habitattype_automatic_assessment', sa.Column('coverage_surface_area_min_max', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('etc_data_habitattype_automatic_assessment', 'percentage_range_trend')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'percentage_hab_condition_trend')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'percentage_coverage_trend')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'percentage_assessment_trend_unfavourable')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_surface_area_min')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_surface_area_max')
