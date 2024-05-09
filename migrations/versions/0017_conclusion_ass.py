revision = "0017"
down_revision = "0016"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "etc_data_habitattype_automatic_assessment",
        sa.Column("conclusion_assessment_prev", sa.String(length=3), nullable=True),
    )
    op.add_column(
        "etc_data_species_automatic_assessment",
        sa.Column("conclusion_assessment_prev", sa.String(length=3), nullable=True),
    )


def downgrade():
    op.drop_column(
        "etc_data_species_automatic_assessment", "conclusion_assessment_prev"
    )
    op.drop_column(
        "etc_data_habitattype_automatic_assessment",
        "conclusion_assessment_prev",
    )
