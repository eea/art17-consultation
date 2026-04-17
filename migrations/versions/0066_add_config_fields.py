"""Add config fields

Revision ID: 0066
Revises: 0065
Create Date: 2026-04-17 09:17:10.772399

"""

from alembic import op
import sqlalchemy as sa


revision = "0066"
down_revision = "0065"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("config", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("default_public_dataset_id", sa.BigInteger(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("add_assessment_enabled", sa.Boolean(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("latest_dataset_public_view_enabled", sa.Boolean(), nullable=True)
        )

    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.add_column(sa.Column("latest", sa.Boolean(), nullable=True))


def downgrade():

    with op.batch_alter_table("datasets", schema=None) as batch_op:
        batch_op.drop_column("latest")

    with op.batch_alter_table("config", schema=None) as batch_op:
        batch_op.drop_column("latest_dataset_public_view_enabled")
        batch_op.drop_column("add_assessment_enabled")
        batch_op.drop_column("default_public_dataset_id")
