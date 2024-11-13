"""Add temporary remote URLs columns for factsheets

Revision ID: 0049
Revises: 0048
Create Date: 2024-11-01 08:29:57.431665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0049"
down_revision = "0048"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "etc_data_species_regions",
        sa.Column("remote_url_2006_new", sa.String(350), nullable=True),
    )
    op.add_column(
        "etc_data_species_regions",
        sa.Column("remote_url_2012_new", sa.String(350), nullable=True),
    )
    op.add_column(
        "etc_data_habitattype_regions",
        sa.Column("remote_url_2006_new", sa.String(350), nullable=True),
    )
    op.add_column(
        "etc_data_habitattype_regions",
        sa.Column("remote_url_2012_new", sa.String(350), nullable=True),
    )


def downgrade():
    op.drop_column("etc_data_species_regions", "remote_url_2006_new")
    op.drop_column("etc_data_species_regions", "remote_url_2012_new")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2006_new")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2012_new")
