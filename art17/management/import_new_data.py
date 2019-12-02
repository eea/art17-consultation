import csv
import sys

from flask_script import Manager, Option
from flask_security.script import Command

from art17 import models

from flask_sqlalchemy import SQLAlchemy
from art17.models import db

def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)
SQLAlchemy.get_model = get_model

class ImportNewDataCommand(Command):

    option_list = Command.option_list + (
        Option('-f', '--file', dest='file', required=True),
        Option('-m', '--model', dest="model", required=True)
    )

    def run(self, **kwargs):
        with open(kwargs['file']) as file:
            data = [{k: v for k, v in row.items()} for row in 
                    csv.DictReader(file, skipinitialspace=True)]
            model_class =  db.get_model(kwargs['model'])
            for data_object in data:
                new_object = model_class(**data_object)
                db.session.add(new_object)
                db.session.commit()

import_new_data = Manager()
import_new_data.add_command('run', ImportNewDataCommand())