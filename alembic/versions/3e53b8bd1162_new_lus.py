revision = '3e53b8bd1162'
down_revision = '5513e75d5036'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('lu_habitattypes_manual_assessments_2007',
        sa.Column('habitatcode', sa.String(length=50), nullable=False),
        sa.Column('region', sa.String(length=4), nullable=False),
        sa.Column('conclusion_assessment', sa.String(length=2), nullable=True),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.PrimaryKeyConstraint('habitatcode', 'region', 'ext_dataset_id')
    )
    op.create_table('lu_species_manual_assessments_2007',
        sa.Column('assesment_speciesname', sa.String(length=60),
                  nullable=False),
        sa.Column('region', sa.String(length=4), nullable=False),
        sa.Column('conclusion_assessment', sa.String(length=2), nullable=True),
        sa.Column('ext_dataset_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['ext_dataset_id'], ['datasets.id'], ),
        sa.PrimaryKeyConstraint('assesment_speciesname', 'region',
                                'ext_dataset_id')
    )


def downgrade():
    op.drop_table('lu_species_manual_assessments_2007')
    op.drop_table('lu_habitattypes_manual_assessments_2007')
