revision = "0011"
down_revision = "0010"

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "datasets",
        sa.Column("schema", sa.String(4), default="2006"),
    )


def downgrade():
    op.drop_column("datasets", "schema")
