revision = '0022'
down_revision = '0021'

from alembic import op
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column('etc_dic_hd_habitats', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)


def downgrade():
    op.alter_column('etc_dic_hd_habitats', 'name',
               existing_type=mysql.VARCHAR(length=155),
               nullable=False)
