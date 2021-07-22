revision = "0025"
down_revision = "0024"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "config", sa.Column("sensitive_species_map_url", sa.String(length=255))
    )


def downgrade():
    op.drop_column("config", "sensitive_species_map_url")
