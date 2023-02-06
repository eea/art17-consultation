revision = "0026"
down_revision = "0025"

from alembic import op

SRC_DATE_FORMAT = "%d/%m/%Y %H:%i"
DST_DATE_FORMAT = "%Y-%m-%d %H:%i"


def get_update_query(table_name):
    return (
        "UPDATE `{tb_name}` SET last_update = "
        "DATE_FORMAT(STR_TO_DATE(last_update, '{src_format}'), '{dst_format}')"
        " WHERE last_update LIKE '%/%';".format(
            tb_name=table_name,
            src_format=SRC_DATE_FORMAT,
            dst_format=DST_DATE_FORMAT,
        )
    )


def upgrade():
    op.execute(get_update_query("species_manual_assessment"))
    op.execute(get_update_query("habitattypes_manual_assessment"))


def downgrade():
    pass
