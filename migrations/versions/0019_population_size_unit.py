revision = "0019"
down_revision = "0018"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "etc_data_species_regions",
        "population_size_unit",
        existing_type=sa.String(length=10),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "etc_data_species_regions",
        "population_size_unit",
        existing_type=sa.String(length=6),
        nullable=True,
    )
