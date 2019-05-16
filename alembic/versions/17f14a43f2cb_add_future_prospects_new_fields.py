revision = '17f14a43f2cb'
down_revision = '277819012155'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions', 
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('structure_future_prospects', sa.String(length=20), nullable=True))

    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('structure_future_prospects', sa.String(length=20), nullable=True))

    op.add_column('habitattypes_manual_assessment',
                  sa.Column('area_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('structure_future_prospects', sa.String(length=20), nullable=True))

    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))

    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('habitat_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))

    op.add_column('species_manual_assessment',
                  sa.Column('habitat_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('population_future_prospects', sa.String(length=20), nullable=True))
    op.add_column('species_manual_assessment',
                  sa.Column('range_future_prospects', sa.String(length=20), nullable=True))


def downgrade():

    op.drop_column('etc_data_species_regions', 'range_future_prospects')
    op.drop_column('etc_data_species_regions', 'population_future_prospects')
    op.drop_column('etc_data_species_regions', 'habitat_future_prospects')

    op.drop_column('etc_data_species_automatic_assessment', 'range_future_prospects')
    op.drop_column('etc_data_species_automatic_assessment', 'population_future_prospects')
    op.drop_column('etc_data_species_automatic_assessment', 'habitat_future_prospects')

    op.drop_column('species_manual_assessment', 'range_future_prospects')
    op.drop_column('species_manual_assessment', 'population_future_prospects')
    op.drop_column('species_manual_assessment', 'habitat_future_prospects')

    op.drop_column('etc_data_habitattype_regions', 'structure_future_prospects')
    op.drop_column('etc_data_habitattype_regions', 'range_future_prospects')
    op.drop_column('etc_data_habitattype_regions', 'population_future_prospects')

    op.drop_column('etc_data_habitattype_automatic_assessment', 'structure_future_prospects')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'range_future_prospects')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'population_future_prospects')

    op.drop_column('habitattypes_manual_assessment', 'structure_future_prospects')
    op.drop_column('habitattypes_manual_assessment', 'range_future_prospects')
    op.drop_column('habitattypes_manual_assessment', 'area_future_prospects')
