revision = 'e55ae0df42c'
down_revision = '49408eeb4094'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('etc_data_species_regions', 'filename',
                  existing_type=sa.String(length=60), type_=sa.String(length=300))


def downgrade():
    op.alter_column('etc_data_species_regions', 'filename',
                  existing_type=sa.String(length=300), type_=sa.String(length=60))