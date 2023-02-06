revision = "0046"
down_revision = "0045"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "datasets",
        "species_map_url",
        existing_type=sa.String(length=255),
        type_=sa.String(length=400),
    )
    op.alter_column(
        "datasets",
        "sensitive_species_map_url",
        existing_type=sa.String(length=255),
        type_=sa.String(length=400),
    )
    op.alter_column(
        "datasets",
        "habitat_map_url",
        existing_type=sa.String(length=255),
        type_=sa.String(length=400),
    )


def downgrade():
    op.alter_column(
        "datasets",
        "species_map_url",
        existing_type=sa.String(length=400),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "datasets",
        "sensitive_species_map_url",
        existing_type=sa.String(length=400),
        type_=sa.String(length=255),
    )
    op.alter_column(
        "datasets",
        "habitat_map_url",
        existing_type=sa.String(length=400),
        type_=sa.String(length=255),
    )
