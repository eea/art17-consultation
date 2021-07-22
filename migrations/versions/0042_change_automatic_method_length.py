revision = "0042"
down_revision = "0041"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        "etc_data_species_automatic_assessment",
        "assessment_method",
        existing_type=sa.String(length=3),
        type_=sa.String(length=10),
    ),


def downgrade():
    op.alter_column(
        "etc_data_species_automatic_assessment",
        "assessment_method",
        existing_type=sa.String(length=10),
        type_=sa.String(length=3),
    ),
