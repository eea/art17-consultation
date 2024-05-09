revision = "0034"
down_revision = "0033"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "complementary_favourable_population_unit",
            sa.String(length=20),
            nullable=True,
        ),
    )

    op.add_column(
        "species_manual_assessment",
        sa.Column("future_habitat", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "species_manual_assessment",
        sa.Column("future_population", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "species_manual_assessment",
        sa.Column("future_range", sa.String(length=20), nullable=True),
    )
    op.drop_column("species_manual_assessment", "population_future_prospects")
    op.drop_column("species_manual_assessment", "range_future_prospects")
    op.drop_column("species_manual_assessment", "habitat_future_prospects")

    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "conclusion_assessment_trend_prev",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("species_manual_assessment", "conclusion_assessment_prev_trend")
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "conclusion_assessment_trend_change",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("species_manual_assessment", "conclusion_assessment_change_trend")
    op.add_column(
        "species_manual_assessment",
        sa.Column("backcasted_2007", sa.String(length=4), nullable=True),
    )
    op.alter_column(
        "species_manual_assessment",
        "population_best_value",
        existing_type=sa.Float(asdecimal=True),
        type_=sa.String(length=23),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_good", sa.String(length=23), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_notgood", sa.String(length=23), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_unknown", sa.String(length=23), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "not_good_structure")
    op.drop_column("habitattypes_manual_assessment", "not_known_structure")
    op.drop_column("habitattypes_manual_assessment", "best_value_area")
    op.drop_column("habitattypes_manual_assessment", "good_structure")
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("future_area", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("future_range", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("future_structure", sa.String(length=20), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "range_future_prospects")
    op.drop_column("habitattypes_manual_assessment", "area_future_prospects")
    op.drop_column("habitattypes_manual_assessment", "structure_future_prospects")
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "conclusion_assessment_trend_change",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "conclusion_assessment_trend_prev",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("habitattypes_manual_assessment", "conclusion_assessment_prev_trend")
    op.drop_column(
        "habitattypes_manual_assessment", "conclusion_assessment_change_trend"
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("backcasted_2007", sa.String(length=4), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("hab_condition_trend", sa.String(length=5), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "trend_structure")


def downgrade():
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("trend_structure", sa.Float(asdecimal=True), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "hab_condition_trend")
    op.drop_column("habitattypes_manual_assessment", "backcasted_2007")
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "conclusion_assessment_change_trend",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column(
            "conclusion_assessment_prev_trend",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("habitattypes_manual_assessment", "conclusion_assessment_trend_prev")
    op.drop_column(
        "habitattypes_manual_assessment", "conclusion_assessment_trend_change"
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("structure_future_prospects", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("area_future_prospects", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("range_future_prospects", sa.String(length=20), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "future_structure")
    op.drop_column("habitattypes_manual_assessment", "future_range")
    op.drop_column("habitattypes_manual_assessment", "future_area")
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("good_structure", sa.Float(asdecimal=True), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("best_value_area", sa.Float(asdecimal=True), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("not_known_structure", sa.Float(asdecimal=True), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("not_good_structure", sa.Float(asdecimal=True), nullable=True),
    )
    op.drop_column("habitattypes_manual_assessment", "hab_condition_unknown")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_notgood")
    op.drop_column("habitattypes_manual_assessment", "hab_condition_good")
    op.alter_column(
        "species_manual_assessment",
        "population_best_value",
        existing_type=sa.String(length=23),
        type_=sa.Float(asdecimal=True),
    )
    op.drop_column("species_manual_assessment", "backcasted_2007")
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "conclusion_assessment_change_trend",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("species_manual_assessment", "conclusion_assessment_trend_change")
    op.add_column(
        "species_manual_assessment",
        sa.Column(
            "conclusion_assessment_prev_trend",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.drop_column("species_manual_assessment", "conclusion_assessment_trend_prev")
    op.add_column(
        "species_manual_assessment",
        sa.Column("habitat_future_prospects", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "species_manual_assessment",
        sa.Column("range_future_prospects", sa.String(length=20), nullable=True),
    )
    op.add_column(
        "species_manual_assessment",
        sa.Column("population_future_prospects", sa.String(length=20), nullable=True),
    )
    op.drop_column("species_manual_assessment", "future_range")
    op.drop_column("species_manual_assessment", "future_population")
    op.drop_column("species_manual_assessment", "future_habitat")
    op.drop_column(
        "species_manual_assessment", "complementary_favourable_population_unit"
    )
