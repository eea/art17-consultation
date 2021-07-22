revision = "0039"
down_revision = "0038"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "etc_data_species_regions",
        "filename",
        existing_type=sa.String(length=60),
        type_=sa.String(length=300),
    )


def downgrade():
    op.alter_column(
        "etc_data_species_regions",
        "filename",
        existing_type=sa.String(length=300),
        type_=sa.String(length=60),
    )
