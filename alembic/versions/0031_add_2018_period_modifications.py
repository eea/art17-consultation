revision = '0031'
down_revision = '0030'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('conclusion_assessment_trend_prev', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('country', sa.String(length=3), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('coverage_estimate_type', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('coverage_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('coverage_surface_area_min_max', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment', 
                  sa.Column('future_area', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('future_range', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('future_structure', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('hab_condition_good', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('hab_condition_notgood', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('hab_condition_trend', sa.String(length=10), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('hab_condition_unknown', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('percentage_assessment_trend_change', sa.String(length=100), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('use_for_statistics', sa.Boolean(), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('conclusion_assessment_trend_change', sa.String(length=20), nullable=True))
    op.alter_column('etc_data_habitattype_regions', 'conclusion_assessment_change',
                  existing_type=sa.String(length=2), type_=sa.String(length=20)),
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('conclusion_assessment_trend_prev', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('presence_new', sa.String(length=60), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('coverage_estimate_type', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('coverage_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('coverage_surface_area_max', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('coverage_surface_area_min', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('coverage_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('distribution_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('future_area', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('future_range', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('future_structure', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_good', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_good_max', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_good_min', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_notgood', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_notgood_max', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_notgood_min', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_trend', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_unknown', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_unknown_max', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('hab_condition_unknown_min', sa.Float(asdecimal=True), nullable=True))
    op.alter_column('etc_data_habitattype_regions', 'range_trend',
                    existing_type=sa.String(length=1), type_=sa.String(length=10)),
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('range_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('use_for_statistics', sa.Boolean(), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('assessment_speciescode', sa.Integer(), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('complementary_favourable_population_unit', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('conclusion_assessment_trend_prev', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('country', sa.String(length=10), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('future_habitat', sa.String(length=200), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('future_population', sa.String(length=200), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('future_range', sa.String(length=200), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('habitat_sufficiency_occupied', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('habitat_sufficiency_unoccupied', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('percentage_assessment_trend_change', sa.String(length=200), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('percentage_habitat_sufficiency', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_estimate_type', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_size_min_max', sa.String(length=100), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_size_unit', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('use_for_statistics', sa.Boolean(), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('assessment_speciescode', sa.Integer(), nullable=True))
    op.alter_column('etc_data_species_regions','assesment_speciesname_changed',
                  new_column_name='assessment_speciesname_changed', existing_type=sa.Integer())
    op.add_column('etc_data_species_regions',
                  sa.Column('complementary_favourable_population_unit', sa.String(length=50), nullable=True))
    op.alter_column('etc_data_species_regions', 'conclusion_assessment_trend', existing_type=sa.String(length=1),
                  type_=sa.String(length=4)),
    op.alter_column('etc_data_species_regions', 'conclusion_assessment_change', existing_type=sa.String(length=2),
                  type_=sa.String(length=20)),
    op.add_column('etc_data_species_regions',
                  sa.Column('conclusion_assessment_trend_change', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('conclusion_assessment_trend_prev', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('presence_new', sa.String(length=60), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('distribution_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('future_habitat', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('future_population', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('future_range', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_sufficiency_method', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_sufficiency_occupied', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_sufficiency_unoccupied', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('popsize_etc', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_alt_estimate_type', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_alt_size', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_alt_size_max', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_alt_size_min', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_alt_size_unit', sa.String(length=10), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_estimate_type', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_size', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_unit', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_units_change', sa.Boolean(), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('range_trend_method', sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('speciescode_IRM', sa.String(length=10), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('use_for_statistics', sa.Boolean(), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('area_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('best_value_area', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('not_good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('not_known_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('structure_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('trend_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('habitat_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_best_value', sa.Float(asdecimal=True), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_unit', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('species_manual_assessment', 'range_future_prospects')
    op.drop_column('species_manual_assessment', 'population_unit')
    op.drop_column('species_manual_assessment', 'population_future_prospects')
    op.drop_column('species_manual_assessment', 'population_best_value')
    op.drop_column('species_manual_assessment', 'habitat_future_prospects')
    op.drop_column('species_manual_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('species_manual_assessment', 'conclusion_assessment_change_trend')
    op.drop_column('habitattypes_manual_assessment', 'trend_structure')
    op.drop_column('habitattypes_manual_assessment', 'structure_future_prospects')
    op.drop_column('habitattypes_manual_assessment', 'range_future_prospects')
    op.drop_column('habitattypes_manual_assessment', 'not_known_structure')
    op.drop_column('habitattypes_manual_assessment', 'not_good_structure')
    op.drop_column('habitattypes_manual_assessment', 'good_structure')
    op.drop_column('habitattypes_manual_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('habitattypes_manual_assessment', 'conclusion_assessment_change_trend')
    op.drop_column('habitattypes_manual_assessment', 'best_value_area')
    op.drop_column('habitattypes_manual_assessment', 'area_future_prospects')
    op.alter_column('etc_data_species_regions','assessment_speciesname_changed',
                  new_column_name='assesment_speciesname_changed', existing_type=sa.Integer())
    op.drop_column('etc_data_species_regions', 'assessment_speciescode')
    op.drop_column('etc_data_species_regions', 'use_for_statistics')
    op.drop_column('etc_data_species_regions', 'speciescode_IRM')
    op.drop_column('etc_data_species_regions', 'range_trend_method')
    op.drop_column('etc_data_species_regions', 'population_units_change')
    op.drop_column('etc_data_species_regions', 'population_unit')
    op.drop_column('etc_data_species_regions', 'population_trend_method')
    op.drop_column('etc_data_species_regions', 'population_size')
    op.drop_column('etc_data_species_regions', 'population_method')
    op.drop_column('etc_data_species_regions', 'population_estimate_type')
    op.drop_column('etc_data_species_regions', 'population_alt_size_unit')
    op.drop_column('etc_data_species_regions', 'population_alt_size_min')
    op.drop_column('etc_data_species_regions', 'population_alt_size_max')
    op.drop_column('etc_data_species_regions', 'population_alt_size')
    op.drop_column('etc_data_species_regions', 'population_alt_estimate_type')
    op.drop_column('etc_data_species_regions', 'popsize_etc')
    op.drop_column('etc_data_species_regions', 'habitat_trend_method')
    op.drop_column('etc_data_species_regions', 'habitat_sufficiency_unoccupied')
    op.drop_column('etc_data_species_regions', 'habitat_sufficiency_occupied')
    op.drop_column('etc_data_species_regions', 'habitat_sufficiency_method')
    op.drop_column('etc_data_species_regions', 'future_range')
    op.drop_column('etc_data_species_regions', 'presence_new')
    op.drop_column('etc_data_species_regions', 'future_population')
    op.drop_column('etc_data_species_regions', 'future_habitat')
    op.drop_column('etc_data_species_regions', 'distribution_method')
    op.drop_column('etc_data_species_regions', 'conclusion_assessment_trend_prev')
    op.drop_column('etc_data_species_regions', 'conclusion_assessment_trend_change')
    op.drop_column('etc_data_species_regions', 'complementary_favourable_population_unit')
    op.alter_column('etc_data_species_regions', 'conclusion_assessment_trend',
                    existing_type=sa.String(length=4), type_=sa.String(length=1))
    op.alter_column('etc_data_species_regions', 'conclusion_assessment_change',
                    existing_type=sa.String(length=20), type_=sa.String(length=2)),
    op.drop_column('etc_data_species_automatic_assessment', 'use_for_statistics')
    op.drop_column('etc_data_species_automatic_assessment', 'population_size_unit')
    op.drop_column('etc_data_species_automatic_assessment', 'population_size_min_max')
    op.drop_column('etc_data_species_automatic_assessment', 'population_method')
    op.drop_column('etc_data_species_automatic_assessment', 'population_estimate_type')
    op.drop_column('etc_data_species_automatic_assessment', 'percentage_habitat_sufficiency')
    op.drop_column('etc_data_species_automatic_assessment', 'percentage_assessment_trend_change')
    op.drop_column('etc_data_species_automatic_assessment', 'habitat_sufficiency_unoccupied')
    op.drop_column('etc_data_species_automatic_assessment', 'habitat_sufficiency_occupied')
    op.drop_column('etc_data_species_automatic_assessment', 'future_range')
    op.drop_column('etc_data_species_automatic_assessment', 'future_population')
    op.drop_column('etc_data_species_automatic_assessment', 'future_habitat')
    op.drop_column('etc_data_species_automatic_assessment', 'country')
    op.drop_column('etc_data_species_automatic_assessment', 'conclusion_assessment_trend_prev')
    op.drop_column('etc_data_species_automatic_assessment', 'complementary_favourable_population_unit')
    op.drop_column('etc_data_species_automatic_assessment', 'assessment_speciescode')
    op.drop_column('etc_data_habitattype_regions', 'use_for_statistics')
    op.drop_column('etc_data_habitattype_regions', 'range_trend_method')
    op.alter_column('etc_data_habitattype_regions', 'range_trend',
                    existing_type=sa.String(length=10), type_=sa.String(length=1)),
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_unknown_min')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_unknown_max')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_unknown')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_trend_method')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_trend')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_notgood_min')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_notgood_max')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_notgood')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_method')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_good_min')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_good_max')
    op.drop_column('etc_data_habitattype_regions', 'hab_condition_good')
    op.drop_column('etc_data_habitattype_regions', 'future_structure')
    op.drop_column('etc_data_habitattype_regions', 'presence_new')
    op.drop_column('etc_data_habitattype_regions', 'future_range')
    op.drop_column('etc_data_habitattype_regions', 'future_area')
    op.drop_column('etc_data_habitattype_regions', 'distribution_method')
    op.drop_column('etc_data_habitattype_regions', 'coverage_trend_method')
    op.drop_column('etc_data_habitattype_regions', 'coverage_surface_area_min')
    op.drop_column('etc_data_habitattype_regions', 'coverage_surface_area_max')
    op.drop_column('etc_data_habitattype_regions', 'coverage_method')
    op.drop_column('etc_data_habitattype_regions', 'coverage_estimate_type')
    op.drop_column('etc_data_habitattype_regions', 'conclusion_assessment_trend_prev')
    op.drop_column('etc_data_habitattype_regions', 'conclusion_assessment_trend_change')
    op.alter_column('etc_data_habitattype_regions', 'conclusion_assessment_change',
                    existing_type=sa.String(length=20), type_=sa.String(length=2)),
    op.drop_column('etc_data_habitattype_automatic_assessment', 'conclusion_assessment_trend_prev')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'country')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_estimate_type')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_method')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'coverage_surface_area_min_max')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'future_area')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'future_range')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'future_structure')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'hab_condition_good')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'hab_condition_notgood')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'hab_condition_trend')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'hab_condition_unknown')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'percentage_assessment_trend_change')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'use_for_statistics')