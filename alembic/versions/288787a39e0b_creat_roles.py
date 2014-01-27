revision = '288787a39e0b'
down_revision = '45579674231a'

from alembic import op
from sqlalchemy.dialects import mysql


def upgrade():
    op.execute(
        "INSERT INTO roles (name, description) VALUES "
        "('admin',       'Administrator'        ), "
        "('etc',         'European topic center'), "
        "('nat',         'National expert'      ), "
        "('stakeholder', 'Stakeholder'          ) "
    )


def downgrade():
    op.execute(
        "DELETE FROM roles WHERE name IN "
        "('admin', 'etc', 'nat', 'stakeholder')"
    )
