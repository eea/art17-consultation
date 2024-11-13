"""Remote temp remote urls columns for factsheets

Revision ID: 0050
Revises: 0050
Create Date: 2024-11-01 14:26:43.526809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0050"
down_revision = "0049"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("etc_data_species_regions", "remote_url_2006_new")
    op.drop_column("etc_data_species_regions", "remote_url_2012_new")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2006_new")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2012_new")


def downgrade():
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
