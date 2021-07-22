revision = "0029"
down_revision = "0028"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "etc_data_habitattype_regions",
        "remote_url_2006",
        existing_type=sa.String(length=350),
        nullable=True,
    )
    op.alter_column(
        "etc_data_habitattype_regions",
        "remote_url_2012",
        existing_type=sa.String(length=350),
        nullable=True,
    )
    op.alter_column(
        "etc_data_species_regions",
        "remote_url_2006",
        existing_type=sa.String(length=350),
        nullable=True,
    )
    op.alter_column(
        "etc_data_species_regions",
        "remote_url_2012",
        existing_type=sa.String(length=350),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        "etc_data_habitattype_regions",
        "remote_url_2006",
        existing_type=sa.String(length=150),
        nullable=True,
    )
    op.alter_column(
        "etc_data_habitattype_regions",
        "remote_url_2012",
        existing_type=sa.String(length=150),
        nullable=True,
    )
    op.alter_column(
        "etc_data_species_regions",
        "remote_url_2006",
        existing_type=sa.String(length=150),
        nullable=True,
    )
    op.alter_column(
        "etc_data_species_regions",
        "remote_url_2012",
        existing_type=sa.String(length=150),
        nullable=True,
    )
