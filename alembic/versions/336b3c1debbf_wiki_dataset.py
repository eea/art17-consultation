revision = '336b3c1debbf'
down_revision = '90a31b5c39b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('wiki_changes',
                  sa.Column('ext_dataset_id', sa.Integer(), nullable=False))
    op.add_column('wiki_trail_changes',
                  sa.Column('ext_dataset_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('wiki_trail_changes', 'ext_dataset_id')
    op.drop_column('wiki_changes', 'ext_dataset_id')
