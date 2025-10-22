"""empty message

Revision ID: 01886d0316f8
Revises: 0053
Create Date: 2025-10-09 09:37:47.856470

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0054"
down_revision = "0053"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("derived_perc_range_FRR", sa.String(length=100), nullable=True)
        )
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
            sa.Column("derived_perc_area_FRA", sa.String(length=100), nullable=True)
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
        batch_op.add_column(
            sa.Column(
                "coverage_trend_magnitude_etc", sa.String(length=100), nullable=True
            )
        )


def downgrade():
    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.drop_column("coverage_trend_magnitude_etc")
        batch_op.drop_column("derived_favourable_reference_area_mean")
        batch_op.drop_column("derived_favourable_reference_area_max")
        batch_op.drop_column("derived_favourable_reference_area_min")
        batch_op.drop_column("derived_perc_area_FRA")
        batch_op.drop_column("derived_favourable_reference_range_mean")
        batch_op.drop_column("derived_favourable_reference_range_max")
        batch_op.drop_column("derived_favourable_reference_range_min")
        batch_op.drop_column("derived_perc_range_FRR")
