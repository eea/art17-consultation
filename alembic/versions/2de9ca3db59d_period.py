
revision = '2de9ca3db59d'
down_revision = '4c5f00269981'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.oracle import NVARCHAR2
from sqlalchemy.sql import table, column


def upgrade():
    op.create_table('datasets',
                    sa.Column('id', sa.Integer, nullable=False),
                    sa.Column('name', NVARCHAR2(255), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
    )
    op.add_column(
        'etc_data_species_regions',
        sa.Column('ext_dataset_id', sa.Integer, nullable=True),
    )
    op.add_column(
        'etc_data_habitattype_regions',
        sa.Column('ext_dataset_id', sa.Integer, nullable=True),
    )

    datasets_table = table('datasets',
                           column('id', sa.Integer),
                           column('name', sa.String),
    )
    op.bulk_insert(datasets_table,
                   [
                       {'id': 1, 'name': '2001-2006'},
                       {'id': 2, 'name': '2007-2012'},
                   ]
    )
    op.execute("UPDATE `etc_data_species_regions` SET `ext_dataset_id`='1'")
    op.execute("UPDATE `etc_data_habitattype_regions` SET `ext_dataset_id`='1'")


def downgrade():
    op.drop_column('etc_data_species_regions', 'ext_dataset_id')
    op.drop_column('etc_data_habitattype_regions', 'ext_dataset_id')
    op.drop_table('datasets')
