revision = '0012'
down_revision = '0011'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column('comments',
                  sa.Column('ext_dataset_id', sa.Integer(), nullable=False))


def downgrade():
    op.drop_column('comments', 'ext_dataset_id')
