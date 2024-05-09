revision = "0012"
down_revision = "0011"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column("comments", sa.Column("ext_dataset_id", sa.Integer(), nullable=False))


def downgrade():
    op.drop_column("comments", "ext_dataset_id")
