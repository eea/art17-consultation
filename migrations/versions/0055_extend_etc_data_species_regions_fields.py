"""empty message

Revision ID: 0055
Revises: 0054
Create Date: 2025-11-17 09:28:57.578952

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0055"
down_revision = "0054"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "priority",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "range_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "habitat_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_trend",
            existing_type=sa.VARCHAR(length=1),
            type_=sa.String(length=10),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_alt_size_unit",
            existing_type=sa.VARCHAR(length=10),
            type_=sa.String(length=20),
            existing_nullable=True,
        )


def downgrade():

    with op.batch_alter_table("etc_data_species_regions", schema=None) as batch_op:
        batch_op.alter_column(
            "priority",
            existing_type=sa.String(length=10),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "range_trend",
            existing_type=sa.String(length=10),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_trend",
            existing_type=sa.String(length=10),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "habitat_trend",
            existing_type=sa.String(length=10),
            type_=sa.VARCHAR(length=1),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "population_alt_size_unit",
            existing_type=sa.String(length=20),
            type_=sa.VARCHAR(length=10),
            existing_nullable=True,
        )
