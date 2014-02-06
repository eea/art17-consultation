revision = '29d441f304e9'
down_revision = '8c833e5565b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.add_column('datasets',
                  sa.Column('schema', sa.String(4), default=2006, nullable=True),
    )


def downgrade():
    op.drop_column('datasets', 'schema')
