revision = '277819012155'
down_revision = '50974899f7aa'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_regions', 
                  sa.Column('distribution_method_area',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('distribution_method_area',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('distribution_method_area',
                  sa.String(length=50), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('distribution_method_area',
                  sa.String(length=50), nullable=True))


def downgrade():
    op.drop_column('etc_data_species_regions', 'distribution_method_area')
    op.drop_column('etc_data_species_automatic_assessment', 'distribution_method_area')
    op.drop_column('etc_data_habitattype_regions', 'distribution_method_area')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'distribution_method_area')
