revision = "0028"
down_revision = "0027"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "etc_data_habitattype_regions",
        sa.Column("remote_url_2006", sa.String(length=150), nullable=True),
    )
    op.add_column(
        "etc_data_habitattype_regions",
        sa.Column("remote_url_2012", sa.String(length=150), nullable=True),
    )
    op.add_column(
        "etc_data_species_regions",
        sa.Column("remote_url_2006", sa.String(length=150), nullable=True),
    )
    op.add_column(
        "etc_data_species_regions",
        sa.Column("remote_url_2012", sa.String(length=150), nullable=True),
    )


def downgrade():
    op.drop_column("etc_data_species_regions", "remote_url_2012")
    op.drop_column("etc_data_species_regions", "remote_url_2006")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2012")
    op.drop_column("etc_data_habitattype_regions", "remote_url_2006")
