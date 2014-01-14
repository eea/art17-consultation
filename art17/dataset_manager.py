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
    model_map = _get_model_map()
    dataset = models.Dataset.query.get(int(dataset_id))
    if dataset is None:
        print "No such dataset"
        return
    for table_name in CLEANUP_TABLES:
        table_model = model_map[table_name]
        table_model.query.filter_by(dataset_id=dataset.id).delete()
    models.db.session.delete(dataset)
    models.db.session.commit()


def stdout_write(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def _get_model_map():
    rv = {}
    for k, model_cls in models.db.Model._decl_class_registry.items():
        if not k.startswith('_'):
            rv[model_cls.__table__.name] = model_cls
    return rv


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
        model_map = _get_model_map()

        with app.app_context():
            input_conn = create_engine(input_db + '?charset=utf8').connect()
            dataset = models.Dataset(name=dataset_name)
            models.db.session.add(dataset)
            models.db.session.flush()

            for table_name, columns in IMPORT_SCHEMA[schema]:
                stdout_write(table_name + ' ')
                out_model = model_map[table_name]
                query = (
                    "SELECT " +
                    ", ".join('`%s`' % c for c in columns) +
                    " FROM `%s`" % table_name
                )
                n = 0
                for in_row in input_conn.execute(query):
                    row_data = dict(in_row.items())
                    out_row = out_model(dataset_id=dataset.id, **row_data)
                    models.db.session.add(out_row)
                    stdout_write('.')
                    n += 1
                stdout_write("\ndone, %d records\n" % n)

                models.db.session.flush()

            if not no_commit:
                models.db.session.commit()

dataset_manager.add_command('import', ImportCommand())


IMPORT_SCHEMA = {
    '2006': [
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
        ]),
    ]
}

CLEANUP_TABLES = set(
    table_name
    for definition in IMPORT_SCHEMA.values()
    for table_name, cols in definition
)
