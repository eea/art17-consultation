revision = '0024'
down_revision = '0023'

from alembic import op
import sqlalchemy as sa

table_pks = [('wiki', ['id']), ('wiki_trail', ['id'])]


def alter_pk(table, pk_fields):
    pk_stmt = ', '.join('`{0}`'.format(pk) for pk in pk_fields)
    op.execute(
        "ALTER TABLE `{0}` DROP PRIMARY KEY, ADD PRIMARY KEY ({1})".format(
            table, pk_stmt)
    )


def upgrade():
    for table, new_pk in table_pks:
        alter_pk(table, new_pk)

    op.add_column('wiki_comments',
                  sa.Column('ext_dataset_id', sa.Integer(), nullable=False))
    op.add_column('wiki_trail_comments',
                  sa.Column('ext_dataset_id', sa.Integer(), nullable=False))


def downgrade():
    op.drop_column('wiki_trail_comments', 'ext_dataset_id')
    op.drop_column('wiki_comments', 'ext_dataset_id')

    for table, new_pk in reversed(table_pks):
        alter_pk(table, new_pk + ['ext_dataset_id'])
