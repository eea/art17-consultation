revision = '0032'
down_revision = '0031'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('etc_data_species_automatic_assessment', 'percentage_habitat_sufficiency',
    existing_type=sa.String(length=20), type_=sa.String(length=100)),

def downgrade():
    op.alter_column('etc_data_species_automatic_assessment', 'percentage_habitat_sufficiency',
    existing_type=sa.String(length=100), type_=sa.String(length=20)),