"""Update EtcDicSpeciesType

Revision ID: 0059
Revises: 0058
Create Date: 2025-12-12 09:15:32.440602

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0059"
down_revision = "0058"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("etc_dic_species_type", schema=None) as batch_op:
        batch_op.alter_column(
            "speciestypeid",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "speciestype",
            existing_type=sa.VARCHAR(length=50),
            type_=sa.String(length=127),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "assesment",
            existing_type=sa.VARCHAR(length=50),
            type_=sa.String(length=127),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "ext_dataset_id",
            existing_type=sa.BIGINT(),
            type_=sa.Integer(),
            existing_nullable=False,
            existing_server_default=sa.text("'0'::bigint"),
        )
        batch_op.create_foreign_key(None, "datasets", ["ext_dataset_id"], ["id"])


def downgrade():
    with op.batch_alter_table("etc_dic_species_type", schema=None) as batch_op:
        batch_op.drop_constraint(None, type_="foreignkey")
        batch_op.alter_column(
            "ext_dataset_id",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=False,
            existing_server_default=sa.text("'0'::bigint"),
        )
        batch_op.alter_column(
            "assesment",
            existing_type=sa.String(length=127),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "speciestype",
            existing_type=sa.String(length=127),
            type_=sa.VARCHAR(length=50),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "speciestypeid",
            existing_type=sa.Integer(),
            type_=sa.BIGINT(),
            existing_nullable=False,
        )
