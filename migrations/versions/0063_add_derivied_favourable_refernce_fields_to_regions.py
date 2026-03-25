"""Add derivied favourable reference fields to regions

Revision ID: 0063
Revises: 0062
Create Date: 2026-03-25 13:08:25.276702

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0063"
down_revision = "0062"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_min",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_max",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_mean",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_area_min",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_area_max",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_area_mean",
                sa.String(length=100),
                nullable=True,
            )
        )

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_min",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_max",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_mean",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_population_min",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_population_max",
                sa.String(length=100),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_population_mean",
                sa.String(length=100),
                nullable=True,
            )
        )


def downgrade():
    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.drop_column("derived_favourable_reference_population_mean")
        batch_op.drop_column("derived_favourable_reference_population_max")
        batch_op.drop_column("derived_favourable_reference_population_min")
        batch_op.drop_column("derived_favourable_reference_range_mean")
        batch_op.drop_column("derived_favourable_reference_range_max")
        batch_op.drop_column("derived_favourable_reference_range_min")

    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.drop_column("derived_favourable_reference_area_mean")
        batch_op.drop_column("derived_favourable_reference_area_max")
        batch_op.drop_column("derived_favourable_reference_area_min")
        batch_op.drop_column("derived_favourable_reference_range_mean")
        batch_op.drop_column("derived_favourable_reference_range_max")
        batch_op.drop_column("derived_favourable_reference_range_min")
