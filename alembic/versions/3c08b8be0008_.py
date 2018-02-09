revision = '3c08b8be0008'
down_revision = '494cfb601afa'

from alembic import op


def upgrade():
    op.alter_column('etc_data_habitattype_automatic_assessment',
                    'ext_dataset_id',
                    default=4)
    op.alter_column('etc_data_habitattype_regions',
                    'ext_dataset_id',
                    default=4)
    op.alter_column('etc_data_species_automatic_assessment',
                    'ext_dataset_id',
                    default=4)
    op.alter_column('etc_data_species_regions',
                    'ext_dataset_id',
                    default=4)


def downgrade():
    op.alter_column('etc_data_habitattype_automatic_assessment',
                    'ext_dataset_id',
                    default=None)
    op.alter_column('etc_data_habitattype_regions',
                    'ext_dataset_id',
                    default=None)
    op.alter_column('etc_data_species_automatic_assessment',
                    'ext_dataset_id',
                    default=None)
    op.alter_column('etc_data_species_regions',
                    'ext_dataset_id',
                    default=None)
