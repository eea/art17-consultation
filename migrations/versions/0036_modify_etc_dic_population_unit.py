revision = "0036"
down_revision = "0035"

from alembic import op
import sqlalchemy as sa


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
