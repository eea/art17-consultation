revision = '0018'
down_revision = '0017'

from alembic import op


def update_pk(table_name, new_pk):
    new_pk_stmt = (', '.join('`%s`' % c for c in new_pk))
    op.execute(
        "ALTER TABLE `%s` " % table_name +
        "DROP PRIMARY KEY, " +
        "ADD PRIMARY KEY (%s)" % new_pk_stmt
    )


def upgrade():
    update_pk('comments', ['id'])
    update_pk('habitat_comments', ['id'])


def downgrade():
    update_pk('habitat_comments', ['id', 'ext_dataset_id'])
    update_pk('comments', ['id', 'ext_dataset_id'])
