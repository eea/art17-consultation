revision = '169e88c7df10'
down_revision = '478762206c3b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        'config',
        sa.Column('sensitive_species_map_url', sa.String(length=255)))


def downgrade():
    op.drop_column('config', 'sensitive_species_map_url')
