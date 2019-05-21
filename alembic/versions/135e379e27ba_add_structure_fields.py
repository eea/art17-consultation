revision = '135e379e27ba'
down_revision = '10ccca49a0f2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_species_regions',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions', 
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))

    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))

    op.add_column('species_manual_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))

    op.add_column('etc_data_habitattype_regions',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))

    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))

    op.add_column('habitattypes_manual_assessment',
                  sa.Column('conclusion_assessment_change_trend', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('conclusion_assessment_prev_trend', sa.String(length=20), nullable=True))



def downgrade():
    op.drop_column('etc_data_species_regions', 'conclusion_assessment_prev_trend')
    op.drop_column('etc_data_species_regions', 'conclusion_assessment_change_trend')

    op.drop_column('etc_data_species_automatic_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('etc_data_species_automatic_assessment', 'conclusion_assessment_change_trend')

    op.drop_column('species_manual_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('species_manual_assessment', 'conclusion_assessment_change_trend')

    op.drop_column('etc_data_habitattype_regions', 'conclusion_assessment_prev_trend')
    op.drop_column('etc_data_habitattype_regions', 'conclusion_assessment_change_trend')

    op.drop_column('etc_data_habitattype_automatic_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'conclusion_assessment_change_trend')

    op.drop_column('habitattypes_manual_assessment', 'conclusion_assessment_prev_trend')
    op.drop_column('habitattypes_manual_assessment', 'conclusion_assessment_change_trend')
