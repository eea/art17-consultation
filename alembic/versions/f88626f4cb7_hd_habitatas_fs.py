revision = 'f88626f4cb7'
down_revision = '2e83cc0c7306'

import os.path
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sql')
SCRIPT_NAME = 'lu_hd_habitats_factsheets.sql'


def upgrade():
    op.create_table(
        'lu_hd_habitats_factsheets',
        sa.Column('habcode', sa.String(length=4), nullable=False),
        sa.Column('group', sa.String(length=40), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=155), nullable=False),
        sa.Column('shortname', sa.String(length=155),
                  nullable=False),
        sa.Column('annex_I_comments', sa.String(length=30),
                  nullable=True),
        sa.Column('marine', sa.Integer(), nullable=True),
        sa.Column('nameheader', sa.String(length=155),
                  nullable=False),
        sa.PrimaryKeyConstraint('habcode')
    )
    with open(os.path.join(SQL_DIR, SCRIPT_NAME)) as f:
        sql = f.read().decode('utf8')
    op.execute(sql)


def downgrade():
    op.drop_table('lu_hd_habitats_factsheets')
