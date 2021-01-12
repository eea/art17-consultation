revision = '0045'
down_revision = '0044'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.alter_column('species_manual_assessment', 'conclusion_assessment_trend_change',
    existing_type=sa.String(length=1), type_=sa.String(length=10))
    op.alter_column('species_manual_assessment', 'conclusion_assessment_change',
    existing_type=sa.String(length=2), type_=sa.String(length=10))
    op.alter_column('habitattypes_manual_assessment', 'conclusion_assessment_trend_change',
    existing_type=sa.String(length=2), type_=sa.String(length=10))
    op.alter_column('habitattypes_manual_assessment', 'conclusion_assessment_change',
    existing_type=sa.String(length=2), type_=sa.String(length=20))


def downgrade():
    op.alter_column('habitattypes_manual_assessment', 'conclusion_assessment_change',
    existing_type=sa.String(length=20), type_=sa.String(length=2))
    op.alter_column('habitattypes_manual_assessment', 'conclusion_assessment_trend_change',
    existing_type=sa.String(length=10), type_=sa.String(length=2))
    op.alter_column('species_manual_assessment', 'conclusion_assessment_change',
    existing_type=sa.String(length=10), type_=sa.String(length=2))
    op.alter_column('species_manual_assessment', 'conclusion_assessment_trend_change',
    existing_type=sa.String(length=10), type_=sa.String(length=1))