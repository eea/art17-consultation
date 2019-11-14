revision = '4727b145f311'
down_revision = 'b895012238'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('etc_data_species_automatic_assessment', 'assessment_method',
    existing_type=sa.String(length=3), type_=sa.String(length=10)),

def downgrade():
    op.alter_column('etc_data_species_automatic_assessment', 'assessment_method',
    existing_type=sa.String(length=10), type_=sa.String(length=3)),