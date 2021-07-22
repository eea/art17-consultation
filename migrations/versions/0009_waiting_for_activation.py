revision = "0009"
down_revision = "0008"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "registered_users",
        sa.Column(
            "waiting_for_activation", sa.Boolean(), server_default="0", nullable=False
        ),
    )


def downgrade():
    op.drop_column("registered_users", "waiting_for_activation")
