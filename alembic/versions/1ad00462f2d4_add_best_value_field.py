revision = '1ad00462f2d4'
down_revision = '494cfb601afa'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment', sa.Column('best_value_area', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_habitattype_regions', sa.Column('best_value_area', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_automatic_assessment', sa.Column('population_best_value', sa.Float(asdecimal=True), nullable=True))
    op.add_column('etc_data_species_regions', sa.Column('population_best_value', sa.Float(asdecimal=True), nullable=True))
    op.add_column('habitattypes_manual_assessment', sa.Column('best_value_area', sa.Float(asdecimal=True), nullable=True))
    op.add_column('species_manual_assessment', sa.Column('population_best_value', sa.Float(asdecimal=True), nullable=True))


def downgrade():
    op.drop_column('species_manual_assessment', 'population_best_value')
    op.drop_column('habitattypes_manual_assessment', 'best_value_area')
    op.drop_column('etc_data_species_regions', 'population_best_value')
    op.drop_column('etc_data_species_automatic_assessment', 'population_best_value')
    op.drop_column('etc_data_habitattype_regions', 'best_value_area')
    op.drop_column('etc_data_habitattype_automatic_assessment', 'best_value_area')
