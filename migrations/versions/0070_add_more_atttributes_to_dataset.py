"""add more atttributes to dataset

Revision ID: 0070
Revises: 0069
Create Date: 2026-07-08 13:04:28.550664

"""
from alembic import op
import sqlalchemy as sa


revision = '0070'
down_revision = '0069'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('datasets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('public_can_view_automatic_assessments', sa.Boolean(), nullable=False, server_default="1"))
        batch_op.add_column(sa.Column('public_can_view_manual_assessments', sa.Boolean(), nullable=False, server_default="1"))

def downgrade():
    with op.batch_alter_table('datasets', schema=None) as batch_op:
        batch_op.drop_column('public_can_view_manual_assessments')
        batch_op.drop_column('public_can_view_automatic_assessments')
