from alembic import op

revision = "0068"
down_revision = "0067"


def upgrade():
    op.execute(
        "UPDATE roles "
        "SET name = 'assessor', description = 'Assessor' "
        "WHERE name = 'etc'"
    )


def downgrade():
    op.execute(
        "UPDATE roles "
        "SET name = 'etc', description = 'European topic center' "
        "WHERE name = 'assessor'"
    )
