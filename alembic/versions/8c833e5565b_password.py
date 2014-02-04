revision = '8c833e5565b'
down_revision = '5922950725a2'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('registered_users',
        sa.Column('password', sa.String(length=60), nullable=True))


def downgrade():
    op.drop_column('registered_users', 'password')
