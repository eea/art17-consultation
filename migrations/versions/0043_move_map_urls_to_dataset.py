revision = "0043"
down_revision = "0042"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.drop_column("config", "species_map_url")
    op.drop_column("config", "sensitive_species_map_url")
    op.drop_column("config", "habitat_map_url")
    op.add_column(
        "datasets",
        sa.Column("habitat_map_url", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("sensitive_species_map_url", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "datasets",
        sa.Column("species_map_url", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("datasets", "species_map_url")
    op.drop_column("datasets", "sensitive_species_map_url")
    op.drop_column("datasets", "habitat_map_url")
    op.add_column(
        "config",
        sa.Column("habitat_map_url", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "config",
        sa.Column("sensitive_species_map_url", sa.String(length=255), nullable=True),
    )
    op.add_column(
        "config",
        sa.Column("species_map_url", sa.String(length=255), nullable=True),
    )
