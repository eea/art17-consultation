revision = '3b4bb34e6a71'
down_revision = '2f76a75a7f00'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('config', sa.Column('default_dataset_id', sa.Integer(),
                                      server_default='1', nullable=True))


def downgrade():
    op.drop_column('config', 'default_dataset_id')
