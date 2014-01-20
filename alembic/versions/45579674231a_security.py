revision = '45579674231a'
down_revision = '18969a5d5c26'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table('roles_users',
        sa.Column('registered_users_user',
                  sa.String(length=50), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['registered_users_user'],
                                ['registered_users.user']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
    )
    op.add_column('registered_users',
        sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('registered_users',
        sa.Column('confirmed_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('registered_users', 'confirmed_at')
    op.drop_column('registered_users', 'active')
    op.drop_table('roles_users')
    op.drop_table('roles')
