revision = "0016"
down_revision = "0015"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "config",
        sa.Column(
            "default_dataset_id",
            sa.Integer(),
            server_default="1",
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("config", "default_dataset_id")
