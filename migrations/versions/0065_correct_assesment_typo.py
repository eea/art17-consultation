"""Correct assesment typo

Revision ID: 0065
Revises: 0064
Create Date: 2026-04-02 08:36:57.083521

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0065"
down_revision = "0064"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=50),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "etc_data_species_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "grouped_assesment",
            new_column_name="grouped_assessment",
            existing_type=sa.Boolean(),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "etc_data_spopulation_pressures", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("etc_data_spopulation_threats", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("etc_dic_species_type", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment",
            new_column_name="assessment",
            existing_type=sa.String(length=127),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "etc_qa_errors_species_manual_checked", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "lu_species_manual_assessments_2007", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("restricted_species", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("species_group", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("species_name", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("wiki", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("wiki_trail", schema=None) as batch_op:
        batch_op.alter_column(
            "assesment_speciesname",
            new_column_name="assessment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )


def downgrade():

    with op.batch_alter_table("wiki_trail", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("wiki", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("species_name", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("species_group", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("restricted_species", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "lu_species_manual_assessments_2007", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "etc_qa_errors_species_manual_checked", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_dic_species_type", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment",
            new_column_name="assesment",
            existing_type=sa.String(length=127),
            existing_nullable=True,
        )

    with op.batch_alter_table("etc_data_spopulation_threats", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "etc_data_spopulation_pressures", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "grouped_assessment",
            new_column_name="grouped_assesment",
            existing_type=sa.Boolean(),
            existing_nullable=True,
        )

    with op.batch_alter_table(
        "etc_data_species_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=60),
            existing_nullable=False,
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.alter_column(
            "assessment_speciesname",
            new_column_name="assesment_speciesname",
            existing_type=sa.String(length=50),
            existing_nullable=False,
        )
