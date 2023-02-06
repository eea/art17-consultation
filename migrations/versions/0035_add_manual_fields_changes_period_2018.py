revision = "0035"
down_revision = "0034"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "complementary_favourable_area_q",
            sa.String(length=2),
            nullable=True,
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "complementary_favourable_range_q",
            sa.String(length=2),
            nullable=True,
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_good_best", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_good_max", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_good_min", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_notgood_best", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_notgood_max", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_notgood_min", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_unknown_best", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_unknown_max", sa.String(length=23), nullable=True
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "hab_condition_unknown_min", sa.String(length=23), nullable=True
        ),
    )
    op.drop_column("habitattypes_manual_assessment", "hab_condition_good")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_notgood")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_unknown")
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "complementary_favourable_population_q",
            sa.String(length=2),
            nullable=True,
        ),
    )
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "complementary_favourable_range_q",
            sa.String(length=2),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column(
        "species_manual_assessment", "complementary_favourable_range_q"
    )
    op.drop_column(
        "species_manual_assessment", "complementary_favourable_population_q"
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_unknown", sa.String(length=23), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_notgood", sa.String(length=23), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_good", sa.String(length=23), nullable=True),
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_unknown_min"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_unknown_max"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_unknown_best"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_notgood_min"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_notgood_max"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "hab_condition_notgood_best"
    )
    op.drop_column("habitattypes_manual_assessment", "hab_condition_good_min")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_good_max")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_good_best")
    op.drop_column(
        "habitattypes_manual_assessment", "complementary_favourable_range_q"
    )
    op.drop_column(
        "habitattypes_manual_assessment", "complementary_favourable_area_q"
    )
