"""empty message

Revision ID: 0051
Revises: 0050
Create Date: 2025-09-12 08:01:23.009510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0051'
down_revision = '0050'
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table('etc_data_species_regions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('derived_favourable_reference_range_combined', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_5_12_b_favourable_reference_range_predefined', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_6_2_e_population_size_class', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_6_4_population_size_quality_of_extrapolation', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_6_11_a_short_term_trend_magnitude_min', sa.Float(asdecimal=True), nullable=True))
        batch_op.add_column(sa.Column('S_6_11_b_short_term_trend_magnitude_max', sa.Float(asdecimal=True), nullable=True))
        batch_op.add_column(sa.Column('S_6_11_c_short_term_trend_magnitude_predefined', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('S_6_11_d_short_term_trend_magnitude_unknown', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('derived_population_size_trend_magnitude', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_6_18_c_favourable_reference_population_unknown', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_population_combined', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_6_18_b_favourable_reference_population_predefined', sa.String(length=23), nullable=True))
        batch_op.add_column(sa.Column('S_7_1_b_habitat_sufficiency_occupied_quality', sa.String(length=25), nullable=True))
        batch_op.add_column(sa.Column('S_7_2_habitat_sufficiency_method_quality', sa.String(length=25), nullable=True))


def downgrade():
    with op.batch_alter_table('etc_data_species_regions', schema=None) as batch_op:
        batch_op.drop_column('S_7_2_habitat_sufficiency_method_quality')
        batch_op.drop_column('S_7_1_b_habitat_sufficiency_occupied_quality')
        batch_op.drop_column('S_6_18_b_favourable_reference_population_predefined')
        batch_op.drop_column('derived_favourable_reference_population_combined')
        batch_op.drop_column('S_6_18_c_favourable_reference_population_unknown')
        batch_op.drop_column('derived_population_size_trend_magnitude')
        batch_op.drop_column('S_6_11_d_short_term_trend_magnitude_unknown')
        batch_op.drop_column('S_6_11_c_short_term_trend_magnitude_predefined')
        batch_op.drop_column('S_6_11_b_short_term_trend_magnitude_max')
        batch_op.drop_column('S_6_11_a_short_term_trend_magnitude_min')
        batch_op.drop_column('S_6_4_population_size_quality_of_extrapolation')
        batch_op.drop_column('S_6_2_e_population_size_class')
        batch_op.drop_column('S_5_12_b_favourable_reference_range_predefined')
        batch_op.drop_column('derived_favourable_reference_range_combined')
