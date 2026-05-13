"""Extend population units field in etc_dic_population_units

Revision ID: 0067
Revises: 0066
Create Date: 2026-05-13 13:09:23.371996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0067'
down_revision = '0066'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('etc_dic_population_units', schema=None) as batch_op:
        batch_op.alter_column('population_units',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=32),
               existing_nullable=False,
               existing_server_default=sa.text("''::character varying"))
        batch_op.alter_column('code',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=32),
               existing_nullable=True)

def downgrade():

    with op.batch_alter_table('etc_dic_population_units', schema=None) as batch_op:
        batch_op.alter_column('code',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
        batch_op.alter_column('population_units',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=16),
               existing_nullable=False,
               existing_server_default=sa.text("''::character varying"))
