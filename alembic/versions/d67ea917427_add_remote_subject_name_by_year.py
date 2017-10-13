revision = 'd67ea917427'
down_revision = '304ad1ec6ca4'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('remote_subject_name_2006',
                            sa.String(length=150), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('remote_subject_name_2012',
                            sa.String(length=150), nullable=True))
    op.drop_column('etc_data_habitattype_regions', 'remote_subject_name')
    op.add_column('etc_data_species_regions',
                  sa.Column('remote_subject_name_2006',
                            sa.String(length=150), nullable=True))
    op.add_column('etc_data_species_regions',
                  sa.Column('remote_subject_name_2012',
                            sa.String(length=150), nullable=True))
    op.drop_column('etc_data_species_regions', 'remote_subject_name')


def downgrade():
    op.add_column('etc_data_species_regions',
                  sa.Column('remote_subject_name',
                            mysql.VARCHAR(length=150), nullable=True))
    op.drop_column('etc_data_species_regions', 'remote_subject_name_2012')
    op.drop_column('etc_data_species_regions', 'remote_subject_name_2006')
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('remote_subject_name',
                            mysql.VARCHAR(length=150), nullable=True))
    op.drop_column('etc_data_habitattype_regions', 'remote_subject_name_2012')
    op.drop_column('etc_data_habitattype_regions', 'remote_subject_name_2006')
