revision = "0030"
down_revision = "0029"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "dic_country_codes", "code", existing_type=sa.String(length=3)
    )

    op.alter_column(
        "dic_country_codes", "codeEU", existing_type=sa.String(length=3)
    )

    op.alter_column("datasets", "schema", existing_type=sa.String(length=7))

    op.alter_column(
        "etc_data_habitattype_regions",
        "eu_country_code",
        existing_type=sa.String(length=3),
    )

    op.alter_column(
        "etc_data_species_regions",
        "eu_country_code",
        existing_type=sa.String(length=3),
    )


def downgrade():

    op.alter_column(
        "etc_data_species_regions",
        "eu_country_code",
        existing_type=sa.String(length=3),
    )

    op.alter_column(
        "etc_data_habitattype_regions",
        "eu_country_code",
        existing_type=sa.String(length=2),
    )

    op.alter_column(
        "dic_country_codes", "code", existing_type=sa.String(length=2)
    )

    op.alter_column(
        "dic_country_codes", "codeEU", existing_type=sa.String(length=2)
    )

    op.alter_column("datasets", "schema", existing_type=sa.String(length=4))
