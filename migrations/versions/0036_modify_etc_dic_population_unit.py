revision = "0036"
down_revision = "0035"

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.alter_column(
        "etc_dic_population_units",
        "population_units",
        existing_type=sa.String(length=6),
        type_=sa.String(length=16),
    ),


def downgrade():
    op.alter_column(
        "etc_dic_population_units",
        "population_units",
        existing_type=sa.String(length=6),
        type_=sa.String(length=16),
    ),
