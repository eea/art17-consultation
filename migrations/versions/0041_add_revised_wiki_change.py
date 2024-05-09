revision = "0041"
down_revision = "0040"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column("wiki_changes", sa.Column("revised", sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column("wiki_changes", "revised")
