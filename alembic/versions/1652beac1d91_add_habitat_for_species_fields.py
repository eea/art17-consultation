revision = '1652beac1d91'
down_revision = '17f14a43f2cb'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('habitat_occupied_sufficiency', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('habitat_unoccupied_sufficiency', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_occupied_sufficiency', sa.String(length=20), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('habitat_unoccupied_sufficiency', sa.String(length=20), nullable=True))

def downgrade():
    op.drop_column('etc_data_species_regions', 'habitat_unoccupied_sufficiency')
    op.drop_column('etc_data_species_regions', 'habitat_occupied_sufficiency')
    op.drop_column('etc_data_species_automatic_assessment', 'habitat_unoccupied_sufficiency')
    op.drop_column('etc_data_species_automatic_assessment', 'habitat_occupied_sufficiency')
