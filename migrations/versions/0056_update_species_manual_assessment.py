"""empty message

Revision ID: 0056
Revises: 0055
Create Date: 2025-11-19 14:44:09.933077

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0056"
down_revision = "0055"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("derived_perc_range_FRR", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(
            sa.Column(
                "derived_population_size_trend_magnitude",
                sa.String(length=23),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "derived_perc_population_FRP", sa.String(length=100), nullable=True
            )
        )
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
    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
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
        batch_op.drop_column("derived_perc_population_FRP")
        batch_op.drop_column("derived_population_size_trend_magnitude")
        batch_op.drop_column("derived_perc_range_FRR")
