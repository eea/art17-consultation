revision = "0010"
down_revision = "0009"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "registered_users",
        sa.Column("password", sa.String(length=60), nullable=True),
    )


def downgrade():
    op.drop_column("registered_users", "password")
