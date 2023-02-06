revision = "0022"
down_revision = "0021"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "etc_dic_hd_habitats",
        "name",
        existing_type=sa.String(length=255),
        nullable=False,
    )


def downgrade():
    op.alter_column(
        "etc_dic_hd_habitats",
        "name",
        existing_type=sa.String(length=155),
        nullable=False,
    )
