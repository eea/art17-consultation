revision = '10ccca49a0f2'
down_revision = '1652beac1d91'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('not_good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('not_known_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions',
                  sa.Column('trend_structure', sa.Float(asdecimal=True), nullable=True))

    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('not_good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('not_known_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('trend_structure', sa.Float(asdecimal=True), nullable=True))

    op.add_column('habitattypes_manual_assessment',
                  sa.Column('good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('not_good_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('not_known_structure', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment',
                  sa.Column('trend_structure', sa.Float(asdecimal=True), nullable=True))

def downgrade():
    op.drop_column('etc_data_habitattype_regions', 'trend_structure')
    op.drop_column('etc_data_habitattype_regions', 'not_known_structure')
    op.drop_column('etc_data_habitattype_regions', 'not_good_structure')
    op.drop_column('etc_data_habitattype_regions', 'good_structure')

    op.drop_column('habitattypes_manual_assessment', 'trend_structure')
    op.drop_column('habitattypes_manual_assessment', 'not_known_structure')
    op.drop_column('habitattypes_manual_assessment', 'not_good_structure')
    op.drop_column('habitattypes_manual_assessment', 'good_structure')

    op.drop_column('etc_data_habitattype_automatic_assessment', 'trend_structure')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'not_known_structure')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'not_good_structure')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'good_structure')
