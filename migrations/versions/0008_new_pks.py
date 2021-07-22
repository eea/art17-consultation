revision = "0008"
down_revision = "0007"

from alembic import op

tables = [
    ("etc_data_habitattype_regions", ["country", "habitatcode", "region"]),
    ("etc_data_species_regions", ["country", "speciescode", "region"]),
]


def update_pk(table_name, old_pk, new_pk):
    new_pk_stmt = ", ".join("`%s`" % c for c in new_pk)
    op.execute(
        "ALTER TABLE `%s` " % table_name
        + "DROP PRIMARY KEY, "
        + "ADD PRIMARY KEY (%s)" % new_pk_stmt
    )


def upgrade():
    for table_name, key_cols in tables:
        update_pk(table_name, key_cols, key_cols + ["ext_dataset_id"])
    op.execute(
        "ALTER TABLE  `etc_data_habitattype_regions` "
        + "CHANGE  `habitattype_type`  `habitattype_type` VARCHAR( 10 )"
    )
    op.execute(
        "ALTER TABLE  `etc_data_species_regions` "
        + "CHANGE  `species_type`  `species_type` VARCHAR( 10 )"
    )


def downgrade():
    for table_name, key_cols in reversed(tables):
        update_pk(table_name, key_cols + ["ext_dataset_id"], key_cols)
    op.execute(
        "ALTER TABLE  `etc_data_habitattype_regions` "
        + "CHANGE  `habitattype_type`  `habitattype_type` VARCHAR( 5 )"
    )
    op.execute(
        "ALTER TABLE  `etc_data_species_regions` "
        + "CHANGE  `species_type`  `species_type` VARCHAR( 5 )"
    )
