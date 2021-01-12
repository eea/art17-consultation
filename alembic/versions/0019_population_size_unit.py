revision = '0019'
down_revision = '0018'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column('etc_data_species_regions', 'population_size_unit',
                    existing_type=mysql.VARCHAR(length=10),
                    nullable=True)


def downgrade():
    op.alter_column('etc_data_species_regions', 'population_size_unit',
                    existing_type=mysql.VARCHAR(length=6),
                    nullable=True)

