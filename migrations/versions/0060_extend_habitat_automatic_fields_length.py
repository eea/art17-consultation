"""empty message

Revision ID: 0060
Revises: 0059
Create Date: 2026-02-02 13:38:43.301327

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0060"
down_revision = "0059"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "order",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good",
            existing_type=sa.VARCHAR(length=50),
            type_=sa.String(length=100),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood",
            existing_type=sa.VARCHAR(length=50),
            type_=sa.String(length=100),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_unknown",
            existing_type=sa.VARCHAR(length=50),
            type_=sa.String(length=100),
            existing_nullable=True,
        )


def downgrade():

    with op.batch_alter_table(
        "etc_data_habitattype_automatic_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "hab_condition_unknown",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_notgood",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "hab_condition_good",
            existing_type=sa.String(length=100),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "order",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=True,
        )
