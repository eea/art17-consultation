import sys
from sqlalchemy import create_engine
from art17 import models
from flask.cli import AppGroup


dataset_manager = AppGroup("dataset")

@dataset_manager.command("ls")
def ls():
    """ List datasets """
    for dataset in models.Dataset.query:
        print(f"{dataset.id}: {dataset.name}")


@dataset_manager.command('rm')
def rm(dataset_id):
    """ Remove a dataset """
    dataset = models.Dataset.query.get(int(dataset_id))
    if dataset is None:
        print("No such dataset")
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


# class ImportCommand(Command):
#     """ Import dataset from another SQL database """

#     def get_options(self):
#         return [
#             Option('-i', '--input_db', required=True),
#             Option('-s', '--schema', required=True),
#             Option('-d', '--dataset_name', required=True),
#             Option('-n', '--no_commit', action='store_true'),
#             Option('-f', '--fallback_dataset', type=int),
#         ]

#     def handle(self, app, input_db, schema,
#                dataset_name, no_commit, fallback_dataset):
#         if schema not in IMPORT_SCHEMA:
#             stdout_write('Unknown schema: %s\n' % schema)
#             return
#         with app.app_context():
#             input_conn = create_engine(input_db + '?charset=utf8', pool_pre_ping=True).connect()
#             dataset = models.Dataset(name=dataset_name, schema=schema)
#             models.db.session.add(dataset)
#             models.db.session.flush()

#             output_conn = models.db.session.connection()

#             for table_name, columns in IMPORT_SCHEMA[schema]:
#                 stdout_write(table_name + ' ... ')
#                 out_columns = columns + ['ext_dataset_id']
#                 columns_sql = ", ".join('`%s`' % c for c in columns)
#                 out_columns_sql = ", ".join('`%s`' % c for c in out_columns)
#                 out_values_sql = ", ".join('%s' for c in out_columns)
#                 query = "SELECT " + columns_sql + " FROM `%s`" % table_name
#                 loaded_from_fallback = False

#                 values = [
#                     list(row) + [dataset.id]
#                     for row in input_conn.execute(query)
#                 ]
#                 if values:
#                     rv = output_conn.execute(
#                         "INSERT INTO `%s` (%s) VALUES (%s)"
#                         % (table_name, out_columns_sql, out_values_sql),
#                         values,
#                     )

#                 elif fallback_dataset and table_name in FALLBACK_TABLES:
#                     values = [
#                         list(row) + [dataset.id]
#                         for row in output_conn.execute(
#                             query +
#                             " WHERE ext_dataset_id = %d" % fallback_dataset
#                         )
#                     ]
#                     if values:
#                         rv = output_conn.execute(
#                             "INSERT INTO `%s` (%s) VALUES (%s)"
#                             % (table_name, out_columns_sql, out_values_sql),
#                             values,
#                         )
#                         loaded_from_fallback = True

#                 stdout_write(str(len(values)))
#                 if loaded_from_fallback:
#                     stdout_write(" (copied from dataset %d)"
#                                  % fallback_dataset)
#                 stdout_write("\n")

#                 models.db.session.flush()

#             if not no_commit:
#                 models.db.session.commit()

# dataset_manager.add_command('import', ImportCommand())


# class UpdateCommand(Command):
#     """ Update particular tables data """

#     def get_options(self):
#         return [
#             Option('-i', '--input_db', required=True),
#             Option('-s', '--schema', required=True),
#             Option('-u', '--update_dataset', required=True),
#             Option('-t', '--tables', nargs='*', required=True),
#             Option('-n', '--no_commit', action='store_true'),
#         ]

#     def handle(self, app, input_db, schema, update_dataset, tables, no_commit):
#         if schema not in IMPORT_SCHEMA:
#             stdout_write('Unknown schema: %s\n' % schema)
#             return
#         with app.app_context():
#             input_conn = create_engine(input_db + '?charset=utf8', pool_pre_ping=True).connect()
#             dataset = models.Dataset.query.get(int(update_dataset))
#             if dataset is None:
#                 stdout_write('Unknown dataset: %s\n' % update_dataset)
#                 return
#             else:
#                 stdout_write('Updating dataset: %s\n' % dataset.name)
#             output_conn = models.db.session.connection()

#             IMPORT_TABLES = []
#             for table_name in tables:
#                 ts = [
#                     columns
#                     for (tn, columns) in IMPORT_SCHEMA[schema]
#                     if tn == table_name
#                 ]
#                 if not ts:
#                     stdout_write('Unknown table_name: %s\n' % table_name)
#                     return
#                 IMPORT_TABLES.append((table_name, ts[0]))

#             for table_name, columns in IMPORT_TABLES:
#                 stdout_write(table_name + ' ... ')
#                 models.db.session.execute(
#                     "DELETE FROM `%s` WHERE ext_dataset_id = %d"
#                     % (table_name, dataset.id)
#                 )
#                 out_columns = columns + ['ext_dataset_id']
#                 columns_sql = ", ".join('`%s`' % c for c in columns)
#                 out_columns_sql = ", ".join('`%s`' % c for c in out_columns)
#                 out_values_sql = ", ".join('%s' for c in out_columns)
#                 query = "SELECT " + columns_sql + " FROM `%s`" % table_name

#                 values = [
#                     list(row) + [dataset.id]
#                     for row in input_conn.execute(query)
#                 ]
#                 if values:
#                     rv = output_conn.execute(
#                         "INSERT INTO `%s` (%s) VALUES (%s)"
#                         % (table_name, out_columns_sql, out_values_sql),
#                         values,
#                     )
#                 stdout_write(str(len(values)))
#                 stdout_write("\n")

#                 models.db.session.flush()
#             if not no_commit:
#                 models.db.session.commit()


# dataset_manager.add_command('update', UpdateCommand())


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
        ('wiki', [
            'id', 'region', 'assesment_speciesname', 'habitatcode']),
        ('wiki_trail', [
            'id', 'region', 'assesment_speciesname', 'habitatcode']),
        ('wiki_changes', [
            'id', 'wiki_id', 'body', 'editor', 'changed', 'active']),
        ('wiki_trail_changes', [
            'id', 'wiki_id', 'body', 'editor', 'changed', 'active']),
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
            'conclusion_assessment_prev',
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
            'conclusion_assessment_prev',
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
        ('lu_species_manual_assessments_2007', [
            'assesment_speciesname', 'region', 'conclusion_assessment',
        ]),
        ('lu_habitattypes_manual_assessments_2007', [
            'habitatcode', 'region', 'conclusion_assessment',
        ]),
    ],
 '2018': [
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
            'conclusion_assessment_prev',
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
            'conclusion_assessment_prev',
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
        ('lu_species_manual_assessments_2007', [
            'assesment_speciesname', 'region', 'conclusion_assessment',
        ]),
        ('lu_habitattypes_manual_assessments_2007', [
            'habitatcode', 'region', 'conclusion_assessment',
        ]),
    ]
}

CLEANUP_TABLES = set(
    table_name
    for definition in IMPORT_SCHEMA.values()
    for table_name, cols in definition
)


CONVERTER_URLS = {
    '2006': {
        'species': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=24&source=remote#{region}',
        'habitat': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=23&source=remote#{region}',
    },
    '2012': {
        'species': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=354&source=remote' +
                   '#{subject}{region}',
        'habitat': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=350&source=remote' +
                   '#{subject}{region}',
    },
    '2012bis': {
        'species': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=354&source=remote' +
                   '#{subject}{region}',
        'habitat': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=350&source=remote' +
                   '#{subject}{region}',
    },
    '2018': {
        'species': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=593&source=remote' +
                   '#{subject}{region}',
        'habitat': '{scheme}://{host}/Converters/run_conversion?' +
                   'file={path}/{filename}&conv=589&source=remote' +
                   '#{subject}{region}',
    },


}


FALLBACK_TABLES = set([
    'dic_country_codes',
    'etc_dic_biogeoreg',
    'etc_dic_conclusion',
    'etc_dic_decision',
    'etc_dic_hd_habitats',
    'etc_dic_method',
    'etc_dic_population_units',
    'etc_dic_species_type',
    'etc_dic_trend',
])
