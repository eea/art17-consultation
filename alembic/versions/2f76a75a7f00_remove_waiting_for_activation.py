revision = '2f76a75a7f00'
down_revision = '1cd5a858fbe9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('registered_users', 'waiting_for_activation')


def downgrade():
    op.add_column('registered_users',
        sa.Column('waiting_for_activation',
            sa.Boolean(), server_default='0', nullable=False))
