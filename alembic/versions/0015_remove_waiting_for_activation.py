revision = '0015'
down_revision = '0014'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_column('registered_users', 'waiting_for_activation')


def downgrade():
    op.add_column('registered_users',
        sa.Column('waiting_for_activation',
            sa.Boolean(), server_default='0', nullable=False))
