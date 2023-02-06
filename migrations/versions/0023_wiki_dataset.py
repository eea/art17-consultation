revision = "0023"
down_revision = "0022"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "wiki_changes",
        sa.Column("ext_dataset_id", sa.Integer(), nullable=False),
    )
    op.add_column(
        "wiki_trail_changes",
        sa.Column("ext_dataset_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("wiki_trail_changes", "ext_dataset_id")
    op.drop_column("wiki_changes", "ext_dataset_id")
