revision = '30882fca6e39'
down_revision = '48b238327773'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column('etc_dic_population_units', 'population_units',
    existing_type=sa.String(length=6), type_=sa.String(length=16)),

def downgrade():
    op.alter_column('etc_dic_population_units', 'population_units',
    existing_type=sa.String(length=6), type_=sa.String(length=16)),