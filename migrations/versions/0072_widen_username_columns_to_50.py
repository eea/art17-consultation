"""Widen username columns from 25 to 50 characters

Usernames may be email addresses (EU Login / Eionet accounts), which overflow
the 25-character columns referencing registered_users.user (itself String(50)).

Revision ID: 0072
Revises: 0071
Create Date: 2026-08-13 11:17:14.243130

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0072"
down_revision = "0071"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.alter_column(
            "user",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "author",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )

    with op.batch_alter_table("comments_read", schema=None) as batch_op:
        batch_op.alter_column(
            "reader_user_id",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )

    with op.batch_alter_table("habitat_comments", schema=None) as batch_op:
        batch_op.alter_column(
            "user",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "author",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )

    with op.batch_alter_table("habitat_comments_read", schema=None) as batch_op:
        batch_op.alter_column(
            "reader_user_id",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "user",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "user_decision",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=True,
        )

    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
        batch_op.alter_column(
            "user",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "user_decision",
            existing_type=sa.VARCHAR(length=25),
            type_=sa.String(length=50),
            existing_nullable=True,
        )


def downgrade():
    with op.batch_alter_table("species_manual_assessment", schema=None) as batch_op:
        batch_op.alter_column(
            "user_decision",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "user",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )

    with op.batch_alter_table(
        "habitattypes_manual_assessment", schema=None
    ) as batch_op:
        batch_op.alter_column(
            "user_decision",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "user",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )

    with op.batch_alter_table("habitat_comments_read", schema=None) as batch_op:
        batch_op.alter_column(
            "reader_user_id",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )

    with op.batch_alter_table("habitat_comments", schema=None) as batch_op:
        batch_op.alter_column(
            "author",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "user",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )

    with op.batch_alter_table("comments_read", schema=None) as batch_op:
        batch_op.alter_column(
            "reader_user_id",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )

    with op.batch_alter_table("comments", schema=None) as batch_op:
        batch_op.alter_column(
            "author",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "user",
            existing_type=sa.String(length=50),
            type_=sa.VARCHAR(length=25),
            existing_nullable=False,
        )
