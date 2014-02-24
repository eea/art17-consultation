revision = '1cd5a858fbe9'
down_revision = '135c9a6d6edc'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('roles', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('roles', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.create_unique_constraint(None, 'roles', ['name'])
    op.create_unique_constraint(None, 'roles', ['description'])


def downgrade():
    op.drop_constraint('name', 'roles', type_='unique')
    op.drop_constraint('description', 'roles', type_='unique')
    op.alter_column('roles', 'name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('roles', 'description',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
