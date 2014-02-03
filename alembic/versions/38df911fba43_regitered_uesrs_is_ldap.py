revision = '38df911fba43'
down_revision = '288787a39e0b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('registered_users',
        sa.Column('is_ldap', sa.Boolean(),
                  server_default='0', nullable=False))


def downgrade():
    op.drop_column('registered_users', 'is_ldap')
