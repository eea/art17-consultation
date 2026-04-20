"""Add derived_perc_range_FRR to habitat manual assessment

Revision ID: 0058
Revises: 0057
Create Date: 2025-12-03 09:32:19.302027

"""

from alembic import op
import sqlalchemy as sa

revision = "0058"
down_revision = "0057"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.add_column(
            sa.Column("derived_perc_range_FRR", sa.String(length=100), nullable=True)
        )
        batch_op.add_column(
            sa.Column("derived_perc_area_FRA", sa.String(length=100), nullable=True)
        )


def downgrade():
    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.drop_column("derived_perc_range_FRR")
        batch_op.drop_column("derived_perc_area_FRA")
