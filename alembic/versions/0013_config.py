revision = '0013'
down_revision = '0012'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('admin_email', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.execute("INSERT INTO config(id) VALUES (1)")


def downgrade():
    op.drop_table('config')
