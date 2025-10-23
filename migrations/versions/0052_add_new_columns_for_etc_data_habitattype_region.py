"""empty message

Revision ID: 0052
Revises: 0051
Create Date: 2025-09-16 12:10:18.629348

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0052"
down_revision = "0051"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "derived_area_trend_magnitude", sa.String(length=23), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_range_combined",
                sa.String(length=23),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "H_4_12_b_favourable_reference_range_predefined",
                sa.String(length=23),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_favourable_reference_area_combined",
                sa.String(length=23),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "H_5_15_b_favourable_reference_area_predefined",
                sa.String(length=23),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_condition_good_mean", sa.Float(asdecimal=True), nullable=True
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_condition_notgood_mean",
                sa.Float(asdecimal=True),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_condition_unknown_mean",
                sa.Float(asdecimal=True),
                nullable=True,
            )
        )


def downgrade():
    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.drop_column("derived_condition_unknown_mean")
        batch_op.drop_column("derived_condition_notgood_mean")
        batch_op.drop_column("derived_condition_good_mean")
        batch_op.drop_column("H_5_15_b_favourable_reference_area_predefined")
        batch_op.drop_column("derived_favourable_reference_area_combined")
        batch_op.drop_column("H_4_12_b_favourable_reference_range_predefined")
        batch_op.drop_column("derived_favourable_reference_range_combined")
        batch_op.drop_column("derived_area_trend_magnitude")
