from flask.ext.script import Manager
from art17 import models

dataset_manager = Manager()


@dataset_manager.command
def ls():
    """ List datasets """
    for dataset in models.Dataset.query:
        print "{d.id}: {d.name}".format(d=dataset)
