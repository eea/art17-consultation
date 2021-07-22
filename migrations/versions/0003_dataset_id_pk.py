revision = "0003"
down_revision = "0002"

from alembic import op

tables = [
    ("dic_country_codes", ["code"]),
    (
        "etc_data_habitattype_automatic_assessment",
        [
            "assessment_method",
            "habitatcode",
            "region",
        ],
    ),
    ("etc_data_habitattype_regions", ["country", "filename", "region"]),
    (
        "etc_data_hcoverage_pressures",
        ["eu_country_code", "region", "habitatcode", "pressure"],
    ),
    (
        "etc_data_hcoverage_threats",
        ["eu_country_code", "region", "habitatcode", "threat"],
    ),
    (
        "etc_data_species_automatic_assessment",
        ["assessment_method", "assesment_speciesname", "region"],
    ),
    ("etc_data_species_regions", ["country", "filename", "region"]),
    (
        "etc_data_spopulation_pressures",
        ["eu_country_code", "region", "n2000_species_code", "pressure"],
    ),
    (
        "etc_data_spopulation_threats",
        ["eu_country_code", "region", "n2000_species_code", "threat"],
    ),
    ("etc_dic_biogeoreg", ["reg_code"]),
    ("etc_dic_conclusion", ["conclusion"]),
    ("etc_dic_decision", ["decision"]),
    ("etc_dic_hd_habitats", ["habcode"]),
    ("etc_dic_method", ["method"]),
    ("etc_dic_population_units", ["population_units"]),
    ("etc_dic_species_type", ["SpeciesTypeID"]),
    ("etc_dic_trend", ["id"]),
    (
        "etc_qa_errors_habitattype_manual_checked",
        ["country", "filename", "region", "error_code"],
    ),
    (
        "etc_qa_errors_species_manual_checked",
        ["country", "filename", "region", "error_code"],
    ),
    ("habitat_comments", ["id"]),
    ("habitattypes_manual_assessment", ["MS", "region", "habitatcode", "user"]),
    ("lu_hd_habitats", ["habcode"]),
    ("photo_habitats", ["id"]),
    ("photo_species", ["id"]),
    ("species_manual_assessment", ["MS", "region", "assesment_speciesname", "user"]),
    ("wiki", ["id"]),
    ("wiki_trail", ["id"]),
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


def downgrade():
    for table_name, key_cols in reversed(tables):
        update_pk(table_name, key_cols + ["ext_dataset_id"], key_cols)
