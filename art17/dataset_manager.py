from flask.ext.script import Manager
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
