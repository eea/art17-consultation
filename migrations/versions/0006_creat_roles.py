revision = "0006"
down_revision = "0005"

from alembic import op


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
        "DELETE FROM roles WHERE name IN " "('admin', 'etc', 'nat', 'stakeholder')"
    )
