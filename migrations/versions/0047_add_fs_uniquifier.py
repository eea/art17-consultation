"""empty message

Revision ID: 473e5957ad5d
Revises: 0046
Create Date: 2021-07-23 15:27:40.126150

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0047"
down_revision = "0046"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "registered_users",
        sa.Column("fs_uniquifier", sa.String(length=255), unique=True),
    )
    # update existing rows with unique fs_uniquifier
    import uuid

    user_table = sa.Table(
        "registered_users",
        sa.MetaData(),
        sa.Column("user", sa.Integer, primary_key=True),
        sa.Column("fs_uniquifier", sa.String),
    )
    conn = op.get_bind()
    for row in conn.execute(sa.select([user_table.c.user])):
        conn.execute(
            user_table.update()
            .values(fs_uniquifier=uuid.uuid4().hex)
            .where(user_table.c.user == row["user"])
        )
    # finally - set nullable to false
    op.alter_column("registered_users", "fs_uniquifier", nullable=False)


def downgrade():
    op.drop_column("registered_users", "fs_uniquifier")
