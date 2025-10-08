"""empty message

Revision ID: 0053
Revises: 0052
Create Date: 2025-10-02 12:48:49.477586

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0053'
down_revision = '0052'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_data_species_automatic_assessment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('derived_perc_range_FRR', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_range_min', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_range_max', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_range_mean', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('population_size_class', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('derived_perc_population_FRP', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('complementary_favourable_population_predefined', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_population_min', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_population_max', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('derived_favourable_reference_population_mean', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('population_trend_magnitude_etc', sa.String(length=100), nullable=True))


def downgrade():
    with op.batch_alter_table('etc_data_species_automatic_assessment', schema=None) as batch_op:
        batch_op.drop_column('population_trend_magnitude_etc')
        batch_op.drop_column('derived_favourable_reference_population_mean')
        batch_op.drop_column('derived_favourable_reference_population_max')
        batch_op.drop_column('derived_favourable_reference_population_min')
        batch_op.drop_column('complementary_favourable_population_predefined')
        batch_op.drop_column('derived_perc_population_FRP')
        batch_op.drop_column('population_size_class')
        batch_op.drop_column('derived_favourable_reference_range_mean')
        batch_op.drop_column('derived_favourable_reference_range_max')
        batch_op.drop_column('derived_favourable_reference_range_min')
        batch_op.drop_column('derived_perc_range_FRR')
