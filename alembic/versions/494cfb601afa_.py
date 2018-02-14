revision = '494cfb601afa'
down_revision = 'b49004f36d5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column('dic_country_codes', 'code',
                    existing_type=mysql.VARCHAR(length=3))

    op.alter_column('dic_country_codes', 'codeEU',
                    existing_type=mysql.VARCHAR(length=3))

    op.alter_column('datasets', 'schema',
                    existing_type=mysql.VARCHAR(length=7))

    op.alter_column('etc_data_habitattype_regions', 'eu_country_code',
                    existing_type=mysql.VARCHAR(length=3))

    op.alter_column('etc_data_species_regions', 'eu_country_code',
                    existing_type=mysql.VARCHAR(length=3))


def downgrade():

    op.alter_column('etc_data_species_regions', 'eu_country_code',
                    existing_type=mysql.VARCHAR(length=3))

    op.alter_column('etc_data_habitattype_regions', 'eu_country_code',
                    existing_type=mysql.VARCHAR(length=2))

    op.alter_column('dic_country_codes', 'code',
                    existing_type=mysql.VARCHAR(length=2))

    op.alter_column('dic_country_codes', 'codeEU',
                    existing_type=mysql.VARCHAR(length=2))

    op.alter_column('datasets', 'schema',
                    existing_type=mysql.VARCHAR(length=4))
