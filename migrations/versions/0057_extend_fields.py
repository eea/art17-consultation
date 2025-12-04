"""Extend fields for import

Revision ID: 0057
Revises: 0056
Create Date: 2025-11-25 11:33:31.067255

"""

from alembic import op
import sqlalchemy as sa

revision = "0057"
down_revision = "0056"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=3),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "H_5_8_a_short_term_trend_magnitude_min",
                sa.String(length=50),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "H_5_8_b_short_term_trend_magnitude_max",
                sa.String(length=50),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "H_5_8_c_short_term_trend_magnitude_predefined",
                sa.String(length=50),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "H_5_8_d_short_term_trend_magnitude_unknown",
                sa.String(length=50),
                nullable=True,
            )
        )
        batch_op.alter_column("delivery", existing_type=sa.BOOLEAN(), nullable=True)
        batch_op.alter_column(
            "envelope", existing_type=sa.VARCHAR(length=50), nullable=True
        )
        batch_op.alter_column(
            "annex_i",
            existing_type=sa.VARCHAR(length=2),
            type_=sa.String(length=5),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=3),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "derived_area_trend_magnitude",
            existing_type=sa.VARCHAR(length=23),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=3),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "etc_data_species_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "order",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=3),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_change",
            existing_type=sa.VARCHAR(length=2),
            type_=sa.String(length=20),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assessment_needed",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column("delivery", existing_type=sa.BOOLEAN(), nullable=True)
        batch_op.alter_column(
            "envelope", existing_type=sa.VARCHAR(length=50), nullable=True
        )
        batch_op.alter_column(
            "tax_order",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_ii_exception",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_iv_exception",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_v_addition",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "eunis_species_code",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "n2000_species_code",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assessment_speciescode",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assessment_speciesname_changed",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_alt_size_unit",
            existing_type=sa.VARCHAR(length=20),
            type_=sa.String(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "complementary_favourable_population_q",
            existing_type=sa.VARCHAR(length=2),
            type_=sa.String(length=4),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_trend_change",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.String(length=20),
            existing_nullable=True,
        )


def downgrade():

    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "conclusion_assessment_trend_change",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.String(length=10),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "complementary_favourable_population_q",
            existing_type=sa.String(length=4),
            type_=sa.VARCHAR(length=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_alt_size_unit",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=20),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assessment_speciesname_changed",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assessment_speciescode",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "n2000_species_code",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "eunis_species_code",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_v_addition",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_iv_exception",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_ii_exception",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "tax_order",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "envelope", existing_type=sa.VARCHAR(length=50), nullable=False
        )
        batch_op.alter_column("delivery", existing_type=sa.BOOLEAN(), nullable=False)

    with op.batch_alter_table(
        "etc_data_species_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assessment_needed",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_change",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.String(length=3),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "order",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_data_habitattype_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.String(length=3),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "derived_area_trend_magnitude",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=23),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "coverage_trend",
            existing_type=sa.String(length=3),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "annex_i",
            existing_type=sa.String(length=5),
            type_=sa.VARCHAR(length=2),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "envelope", existing_type=sa.VARCHAR(length=50), nullable=False
        )
        batch_op.alter_column("delivery", existing_type=sa.BOOLEAN(), nullable=False)
        batch_op.drop_column("H_5_8_d_short_term_trend_magnitude_unknown")
        batch_op.drop_column("H_5_8_c_short_term_trend_magnitude_predefined")
        batch_op.drop_column("H_5_8_b_short_term_trend_magnitude_max")
        batch_op.drop_column("H_5_8_a_short_term_trend_magnitude_min")

    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "conclusion_assessment_trend",
            existing_type=sa.String(length=3),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
