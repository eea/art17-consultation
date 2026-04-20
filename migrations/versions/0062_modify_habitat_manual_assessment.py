"""Modify habitat_manual_assessment

Revision ID: 0063
Revises: 0061
Create Date: 2026-03-06 08:26:09.916130

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0062"
down_revision = "0061"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("hab_condition_good", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column("hab_condition_notgood", sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column("hab_condition_unknown", sa.String(length=50), nullable=True)
        )
        batch_op.alter_column(
            "range_surface_area",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "range_yearly_magnitude",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "complementary_favourable_range",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area_min",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area_max",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_yearly_magnitude",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "complementary_favourable_area",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_min",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_max",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_best",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_min",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_max",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_best",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown_min",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown_max",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown_best",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "hab_condition_unknown_best",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown_max",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown_min",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_best",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_max",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood_min",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_best",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_max",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good_min",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "complementary_favourable_area",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_yearly_magnitude",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area_max",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area_min",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_surface_area",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "complementary_favourable_range",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "range_yearly_magnitude",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "range_surface_area",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.drop_column("hab_condition_unknown")
        batch_op.drop_column("hab_condition_notgood")
        batch_op.drop_column("hab_condition_good")
