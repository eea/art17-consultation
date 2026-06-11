import sqlalchemy as sa
from alembic import op

revision = "0025"
down_revision = "0024"


def upgrade():
    op.add_column(
        "config", sa.Column("sensitive_species_map_url", sa.String(length=255))
    )


def downgrade():
    op.drop_column("config", "sensitive_species_map_url")
