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

class FixBgLinkCommand(Command):

    def run(self, **kwargs):
        link = ''
        species = models.EtcDataSpeciesRegion.query.filter_by(country='BG', dataset_id=5)
        habitats = models.EtcDataHabitattypeRegion.query.filter_by(country='BG', dataset_id=5)
        # for specie in species:
        #     specie.filename = link
        #     db.session.add(specie)
        #     db.session.commit()
        
        for habitat in habitats:
            habitat.filename = link
            db.session.add(habitat)
            db.session.commit()

fix_bg_link = Manager()
fix_bg_link.add_command('run', FixBgLinkCommand())