revision = '12eb89fce058'
down_revision = '3b4bb34e6a71'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('etc_data_habitattype_automatic_assessment',
                  sa.Column('conclusion_assessment_prev', sa.String(length=3),
                            nullable=True))
    op.add_column('etc_data_species_automatic_assessment',
                  sa.Column('conclusion_assessment_prev', sa.String(length=3),
                            nullable=True))


def downgrade():
    op.drop_column('etc_data_species_automatic_assessment',
                   'conclusion_assessment_prev')
    op.drop_column('etc_data_habitattype_automatic_assessment',
                   'conclusion_assessment_prev')
