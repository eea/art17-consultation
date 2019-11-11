revision = 'b895012238'
down_revision = '2502420956c9'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('wiki_changes', sa.Column('revised', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('wiki_changes', 'revised')
