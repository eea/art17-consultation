import sys
from flask.ext.script import Manager, Command, Option
from sqlalchemy import create_engine
from art17 import models

dataset_manager = Manager()


@dataset_manager.command
def ls():
    """ List datasets """
    for dataset in models.Dataset.query:
        print "{d.id}: {d.name}".format(d=dataset)


@dataset_manager.command
def rm(dataset_id):
    """ Remove a dataset """
    dataset = models.Dataset.query.get(int(dataset_id))
    if dataset is None:
        print "No such dataset"
        return
    for table_name in CLEANUP_TABLES:
        models.db.session.execute(
            "DELETE FROM `%s` WHERE ext_dataset_id = %d"
            % (table_name, dataset.id)
        )
    models.db.session.delete(dataset)
    models.db.session.commit()


def stdout_write(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


class ImportCommand(Command):
    """ Import dataset from another SQL database """

    def get_options(self):
        return [
            Option('-i', '--input_db', required=True),
            Option('-s', '--schema', required=True),
            Option('-d', '--dataset_name', required=True),
            Option('-n', '--no_commit', action='store_true'),
        ]

    def handle(self, app, input_db, schema, dataset_name, no_commit):
        with app.app_context():
            input_conn = create_engine(input_db + '?charset=utf8').connect()
            dataset = models.Dataset(name=dataset_name)
            models.db.session.add(dataset)
            models.db.session.flush()

            for table_name, columns in IMPORT_SCHEMA[schema]:
                stdout_write(table_name + ' ... ')
                out_columns = columns + ['ext_dataset_id']
                columns_sql = ", ".join('`%s`' % c for c in columns)
                out_columns_sql = ", ".join('`%s`' % c for c in out_columns)
                out_values_sql = ", ".join('%s' for c in out_columns)
                query = "SELECT " + columns_sql + " FROM `%s`" % table_name

                values = [
                    list(row) + [dataset.id]
                    for row in input_conn.execute(query)
                ]
                if values:
                    rv = models.db.session.connection().execute(
                        "INSERT INTO `%s` (%s) VALUES (%s)"
                        % (table_name, out_columns_sql, out_values_sql),
                        values,
                    )

                stdout_write("%d\n" % len(values))

                models.db.session.flush()

            if not no_commit:
                models.db.session.commit()

dataset_manager.add_command('import', ImportCommand())


IMPORT_SCHEMA = {
    '2006': [
        ('dic_country_codes', [
            'code', 'codeEU', 'name']),
        ('etc_data_habitattype_automatic_assessment', [
            'assessment_method', 'order', 'habitatcode', 'region',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'coverage_surface_area',
            'percentage_coverage_surface_area', 'coverage_trend',
            'coverage_yearly_magnitude', 'complementary_favourable_area',
            'conclusion_range', 'conclusion_range_gis', 'conclusion_coverage',
            'conclusion_coverage_gis', 'percentage_structure',
            'conclusion_structure', 'percentage_future', 'conclusion_future',
            'percentage_assessment', 'conclusion_assessment',
            'range_grid_area', 'percentage_range_grid_area',
            'distribution_grid_area', 'percentage_distribution_grid_area',
            'assessment_needed']),
        ('etc_data_habitattype_regions', [
            'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
            'region', 'region_ms', 'region_changed', 'group', 'annex',
            'annex_I', 'priority', 'code', 'habitatcode', 'habitattype_type',
            'habitattype_type_asses', 'range_surface_area',
            'percentage_range_surface_area', 'range_trend',
            'range_yearly_magnitude', 'complementary_favourable_range_q',
            'complementary_favourable_range', 'coverage_surface_area',
            'percentage_coverage_surface_area', 'coverage_trend',
            'coverage_yearly_magnitude', 'complementary_favourable_area_q',
            'complementary_favourable_area', 'conclusion_range',
            'conclusion_area', 'conclusion_structure', 'conclusion_future',
            'conclusion_assessment', 'range_quality', 'coverage_quality',
            'complementary_other_information',
            'complementary_other_information_english', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area']),
        ('etc_data_hcoverage_pressures', [
            'eu_country_code', 'region', 'habitatcode', 'pressure']),
        ('etc_data_hcoverage_threats', [
            'eu_country_code', 'region', 'habitatcode', 'threat']),
        ('etc_data_species_automatic_assessment', [
            'assessment_method', 'order', 'assesment_speciesname', 'region',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'population_size',
            'percentage_population_mean_size', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population', 'habitat_surface_area',
            'percentage_habitat_surface_area', 'habitat_trend',
            'complementary_suitable_habitat', 'percentage_future',
            'conclusion_range', 'conclusion_range_gis',
            'conclusion_population', 'conclusion_population_gis',
            'conclusion_habitat', 'conclusion_habitat_gis',
            'conclusion_future', 'percentage_assessment',
            'conclusion_assessment', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area', 'assessment_needed']),
        ('etc_data_species_regions', [
            'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
            'region', 'region_ms', 'region_was_changed', 'group', 'tax_group',
            'tax_order', 'upper_group', 'mid_group', 'family', 'annex',
            'annex_II', 'annex_II_exception', 'priority', 'annex_IV',
            'annex_IV_exception', 'annex_V', 'annex_V_addition', 'code',
            'speciescode', 'speciesname', 'species_name_different',
            'eunis_species_code', 'valid_speciesname', 'n2000_species_code',
            'assesment_speciesname', 'assesment_speciesname_changed',
            'grouped_assesment', 'species_type', 'species_type_asses',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range_q',
            'complementary_favourable_range', 'population_minimum_size',
            'percentage_population_minimum_size', 'population_maximum_size',
            'percentage_population_maximum_size', 'filled_population',
            'population_size_unit', 'number_of_different_population_units',
            'different_population_percentage',
            'percentage_population_mean_size', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population_q',
            'complementary_favourable_population',
            'filled_complementary_favourable_population',
            'habitat_surface_area', 'percentage_habitat_surface_area',
            'habitat_trend', 'complementary_suitable_habitat',
            'future_prospects', 'conclusion_range', 'conclusion_population',
            'conclusion_habitat', 'conclusion_future', 'conclusion_assessment',
            'range_quality', 'population_quality', 'habitat_quality',
            'complementary_other_information',
            'complementary_other_information_english', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area']),
        ('etc_data_spopulation_pressures', [
            'eu_country_code', 'region', 'n2000_species_code',
            'assesment_speciesname', 'pressure']),
        ('etc_data_spopulation_threats', [
            'eu_country_code', 'region', 'n2000_species_code',
            'assesment_speciesname', 'threat']),
        ('etc_dic_biogeoreg', [
            'reg_code', 'reg_name', 'ordine', 'order']),
        ('etc_dic_conclusion', [
            'order', 'conclusion', 'details']),
        ('etc_dic_decision', [
            'order', 'decision', 'details']),
        ('etc_dic_hd_habitats', [
            'habcode', 'group', 'priority', 'name', 'shortname',
            'annex_I_comments', 'marine']),
        ('etc_dic_method', [
            'order', 'method', 'details']),
        ('etc_dic_population_units', [
            'order', 'population_units', 'details', 'code']),
        ('etc_dic_species_type', [
            'SpeciesTypeID', 'SpeciesType', 'Assesment', 'Note', 'abbrev']),
        ('etc_dic_trend', [
            'id', 'trend', 'details']),
        ('etc_qa_errors_habitattype_manual_checked', [
            'country', 'eu_country_code', 'filename', 'region', 'habitatcode',
            'suspect_value', 'error_code', 'error_description', 'FlagField',
            'FlagText']),
        ('etc_qa_errors_species_manual_checked', [
            'country', 'eu_country_code', 'filename', 'region',
            'assesment_speciesname', 'suspect_value', 'error_code',
            'error_description', 'FlagField', 'FlagText']),
        #('habitat_comments', [
        #    'id', 'region', 'habitat', 'user', 'MS', 'comment', 'author',
        #    'post_date', 'deleted']),
        #('habitats2eunis', [
        #    'CODE_2000', 'ID_HABITAT']),
        ('habitattypes_manual_assessment', [
           'MS', 'region', 'habitatcode', 'range_surface_area', 'range_trend',
           'range_yearly_magnitude', 'complementary_favourable_range',
           'coverage_surface_area', 'coverage_trend',
           'coverage_yearly_magnitude', 'complementary_favourable_area',
           'method_range', 'conclusion_range', 'method_area',
           'conclusion_area', 'method_structure', 'conclusion_structure',
           'method_future', 'conclusion_future', 'method_assessment',
           'conclusion_assessment', 'user', 'last_update', 'deleted_record',
           'decision', 'user_decision', 'last_update_decision']),
        ('lu_hd_habitats', [
            'habcode', 'group', 'priority', 'name', 'annex_I_comments',
            'marine']),
        #('photo_habitats', [
        #    'id', 'habitatcode', 'description', 'photographer', 'location',
        #    'content_type', 'picture_date', 'picture_data', 'thumbnail',
        #    'user']),
        ('photo_species', [
            'id', 'assessment_speciesname', 'description', 'photographer',
            'location', 'karma', 'content_type', 'picture_date',
            'picture_data', 'thumbnail', 'user']),
        ('restricted_habitats', [
            'habitatcode', 'eu_country_code', 'show_data']),
        ('restricted_species', [
            'assesment_speciesname', 'eu_country_code', 'show_data']),
        ('species_manual_assessment', [
            'MS', 'region', 'assesment_speciesname', 'range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'population_size',
            'population_size_unit', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population', 'habitat_surface_area',
            'habitat_trend', 'complementary_suitable_habitat', 'method_range',
            'conclusion_range', 'method_population', 'conclusion_population',
            'method_habitat', 'conclusion_habitat', 'method_future',
            'conclusion_future', 'method_assessment', 'conclusion_assessment',
            'user', 'last_update', 'deleted_record', 'decision',
            'user_decision', 'last_update_decision']),
        #('wiki', [
        #    'id', 'region', 'assesment_speciesname', 'habitatcode']),
        #('wiki_trail', [
        #    'id', 'region', 'assesment_speciesname', 'habitatcode']),
    ],
    '2012': [
        ('dic_country_codes', [
            'code', 'codeEU', 'name']),
        ('etc_data_habitattype_automatic_assessment', [
            'assessment_method', 'order', 'habitatcode', 'region',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'coverage_surface_area',
            'percentage_coverage_surface_area', 'coverage_trend',
            'coverage_yearly_magnitude', 'complementary_favourable_area',
            'conclusion_range', 'conclusion_range_gis', 'conclusion_coverage',
            'conclusion_coverage_gis', 'percentage_structure',
            'conclusion_structure', 'percentage_future', 'conclusion_future',
            'percentage_assessment', 'conclusion_assessment',
            'range_grid_area', 'percentage_range_grid_area',
            'distribution_grid_area', 'percentage_distribution_grid_area',
            'assessment_needed',
            'percentage_assessment_trend', 'conclusion_assessment_trend',
            'percentage_assessment_change', 'conclusion_assessment_change',
            ]),
        ('etc_data_habitattype_regions', [
            'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
            'region', 'region_ms', 'region_changed', 'group', 'annex',
            'annex_I', 'priority', 'code', 'habitatcode', 'habitattype_type',
            'habitattype_type_asses', 'range_surface_area',
            'percentage_range_surface_area', 'range_trend',
            'range_yearly_magnitude', 'complementary_favourable_range_q',
            'complementary_favourable_range', 'coverage_surface_area',
            'percentage_coverage_surface_area', 'coverage_trend',
            'coverage_yearly_magnitude', 'complementary_favourable_area_q',
            'complementary_favourable_area', 'conclusion_range',
            'conclusion_area', 'conclusion_structure', 'conclusion_future',
            'conclusion_assessment', 'range_quality', 'coverage_quality',
            'complementary_other_information',
            'complementary_other_information_english', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area',
            'range_change_reason', 'coverage_change_reason',
            'conclusion_assessment_trend', 'conclusion_assessment_prev',
            'conclusion_assessment_change',
            ]),
        ('etc_data_hcoverage_pressures', [
            'eu_country_code', 'region', 'habitatcode', 'pressure']),
        ('etc_data_hcoverage_threats', [
            'eu_country_code', 'region', 'habitatcode', 'threat']),
        ('etc_data_species_automatic_assessment', [
            'assessment_method', 'order', 'assesment_speciesname', 'region',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'population_size',
            'percentage_population_mean_size', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population', 'habitat_surface_area',
            'percentage_habitat_surface_area', 'habitat_trend',
            'complementary_suitable_habitat', 'percentage_future',
            'conclusion_range', 'conclusion_range_gis',
            'conclusion_population', 'conclusion_population_gis',
            'conclusion_habitat', 'conclusion_habitat_gis',
            'conclusion_future', 'percentage_assessment',
            'conclusion_assessment', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area', 'assessment_needed',
            'percentage_assessment_trend', 'conclusion_assessment_trend',
            'percentage_assessment_change', 'conclusion_assessment_change',
            ]),
        ('etc_data_species_regions', [
            'country', 'eu_country_code', 'delivery', 'envelope', 'filename',
            'region', 'region_ms', 'region_was_changed', 'group', 'tax_group',
            'tax_order', 'upper_group', 'mid_group', 'family', 'annex',
            'annex_II', 'annex_II_exception', 'priority', 'annex_IV',
            'annex_IV_exception', 'annex_V', 'annex_V_addition', 'code',
            'speciescode', 'speciesname', 'species_name_different',
            'eunis_species_code', 'valid_speciesname', 'n2000_species_code',
            'assesment_speciesname', 'assesment_speciesname_changed',
            'grouped_assesment', 'species_type', 'species_type_asses',
            'range_surface_area', 'percentage_range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range_q',
            'complementary_favourable_range', 'population_minimum_size',
            'percentage_population_minimum_size', 'population_maximum_size',
            'percentage_population_maximum_size', 'filled_population',
            'population_size_unit', 'number_of_different_population_units',
            'different_population_percentage',
            'percentage_population_mean_size', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population_q',
            'complementary_favourable_population',
            'filled_complementary_favourable_population',
            'habitat_surface_area', 'percentage_habitat_surface_area',
            'habitat_trend', 'complementary_suitable_habitat',
            'future_prospects', 'conclusion_range', 'conclusion_population',
            'conclusion_habitat', 'conclusion_future', 'conclusion_assessment',
            'range_quality', 'population_quality', 'habitat_quality',
            'complementary_other_information',
            'complementary_other_information_english', 'range_grid_area',
            'percentage_range_grid_area', 'distribution_grid_area',
            'percentage_distribution_grid_area',
            'range_change_reason', 'population_change_reason',
            'habitat_change_reason',
            'population_units_agreed', 'population_units_other',
            'conclusion_assessment_trend', 'conclusion_assessment_prev',
            'conclusion_assessment_change',
            ]),
        ('etc_data_spopulation_pressures', [
            'eu_country_code', 'region', 'n2000_species_code',
            'assesment_speciesname', 'pressure']),
        ('etc_data_spopulation_threats', [
            'eu_country_code', 'region', 'n2000_species_code',
            'assesment_speciesname', 'threat']),
        ('etc_dic_biogeoreg', [
            'reg_code', 'reg_name', 'ordine', 'order']),
        ('etc_dic_conclusion', [
            'order', 'conclusion', 'details']),
        ('etc_dic_decision', [
            'order', 'decision', 'details']),
        ('etc_dic_hd_habitats', [
            'habcode', 'group', 'priority', 'name', 'shortname',
            'annex_I_comments', 'marine']),
        ('etc_dic_method', [
            'order', 'method', 'details']),
        ('etc_dic_population_units', [
            'order', 'population_units', 'details', 'code']),
        ('etc_dic_species_type', [
            'SpeciesTypeID', 'SpeciesType', 'Assesment', 'Note', 'abbrev']),
        ('etc_dic_trend', [
            'id', 'trend', 'details']),
        ('etc_qa_errors_habitattype_manual_checked', [
            'country', 'eu_country_code', 'filename', 'region', 'habitatcode',
            'suspect_value', 'error_code', 'error_description', 'FlagField',
            'FlagText']),
        ('etc_qa_errors_species_manual_checked', [
            'country', 'eu_country_code', 'filename', 'region',
            'assesment_speciesname', 'suspect_value', 'error_code',
            'error_description', 'FlagField', 'FlagText']),
        ('habitattypes_manual_assessment', [
            'MS', 'region', 'habitatcode', 'range_surface_area', 'range_trend',
            'range_yearly_magnitude', 'complementary_favourable_range',
            'coverage_surface_area', 'coverage_trend',
            'coverage_yearly_magnitude', 'complementary_favourable_area',
            'method_range', 'conclusion_range', 'method_area',
            'conclusion_area', 'method_structure', 'conclusion_structure',
            'method_future', 'conclusion_future', 'method_assessment',
            'conclusion_assessment', 'user', 'last_update', 'deleted_record',
            'decision', 'user_decision', 'last_update_decision',
            'conclusion_assessment_trend', 'conclusion_assessment_prev',
            'conclusion_assessment_change',
            'conclusion_target1', 'method_target1',
        ]),
        ('lu_hd_habitats', [
            'habcode', 'group', 'priority', 'name', 'annex_I_comments',
            'marine']),
        ('photo_species', [
            'id', 'assessment_speciesname', 'description', 'photographer',
            'location', 'karma', 'content_type', 'picture_date',
            'picture_data', 'thumbnail', 'user']),
        ('restricted_habitats', [
            'habitatcode', 'eu_country_code', 'show_data']),
        ('restricted_species', [
            'assesment_speciesname', 'eu_country_code', 'show_data']),
        ('species_manual_assessment', [
            'MS', 'region', 'assesment_speciesname', 'range_surface_area',
            'range_trend', 'range_yearly_magnitude',
            'complementary_favourable_range', 'population_size',
            'population_size_unit', 'population_trend',
            'population_yearly_magnitude',
            'complementary_favourable_population', 'habitat_surface_area',
            'habitat_trend', 'complementary_suitable_habitat', 'method_range',
            'conclusion_range', 'method_population', 'conclusion_population',
            'method_habitat', 'conclusion_habitat', 'method_future',
            'conclusion_future', 'method_assessment', 'conclusion_assessment',
            'user', 'last_update', 'deleted_record', 'decision',
            'user_decision', 'last_update_decision',
            'conclusion_assessment_trend', 'conclusion_assessment_prev',
            'conclusion_assessment_change',
            'conclusion_target1', 'method_target1',
        ]),
    ]
}

CLEANUP_TABLES = set(
    table_name
    for definition in IMPORT_SCHEMA.values()
    for table_name, cols in definition
)
