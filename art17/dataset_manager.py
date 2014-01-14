from flask.ext.script import Manager, Command, Option
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
    models.db.session.delete(dataset)
    models.db.session.commit()


class ImportCommand(Command):
    """ Import dataset from another SQL database """

    def get_options(self):
        return [
            Option('-s', '--source', required=True),
            Option('-d', '--dataset_name', required=True),
            Option('-n', '--no_commit', action='store_true'),
        ]

    def handle(self, app, source, dataset_name, no_commit):
        with app.app_context():
            dataset = models.Dataset(name=dataset_name)
            models.db.session.add(dataset)

            if not no_commit:
                models.db.session.commit()

dataset_manager.add_command('import', ImportCommand())
