revision = "0005"
down_revision = "0004"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "species_manual_assessment",
        sa.Column("method_target1", sa.String(length=3), nullable=True),
    )
    op.add_column(
        "habitattypes_manual_assessment",
        sa.Column("method_target1", sa.String(length=3), nullable=True),
    )


def downgrade():
    op.drop_column("species_manual_assessment", "method_target1")
    op.drop_column("habitattypes_manual_assessment", "method_target1")
