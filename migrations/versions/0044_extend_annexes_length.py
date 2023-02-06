revision = "0044"
down_revision = "0043"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "etc_data_species_regions",
        "annex_II",
        existing_type=sa.String(length=2),
        type_=sa.String(length=5),
    )
    op.alter_column(
        "etc_data_species_regions",
        "annex_IV",
        existing_type=sa.String(length=2),
        type_=sa.String(length=5),
    )
    op.alter_column(
        "etc_data_species_regions",
        "annex_V",
        existing_type=sa.String(length=2),
        type_=sa.String(length=5),
    )


def downgrade():
    op.alter_column(
        "etc_data_species_regions",
        "annex_V",
        existing_type=sa.String(length=5),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_species_regions",
        "annex_IV",
        existing_type=sa.String(length=5),
        type_=sa.String(length=2),
    )
    op.alter_column(
        "etc_data_species_regions",
        "annex_II",
        existing_type=sa.String(length=5),
        type_=sa.String(length=2),
    )
