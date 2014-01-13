revision = '4c5f00269981'
down_revision = None

import os
from alembic import op

SQL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sql')
SCRIPT_NAME = 'art17_consultation_2014-01-08.sql'


def upgrade():
    with open(os.path.join(SQL_DIR, SCRIPT_NAME)) as f:
        sql = f.read()
    op.execute(sql)


def downgrade():
    raise NotImplementedError("Just drop & create the database manually.")
