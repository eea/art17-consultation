from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy

from art17.models import EtcDataHabitattypeRegion, EtcDataSpeciesRegion, db


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


SQLAlchemy.get_model = get_model


fix_bg_link = AppGroup("fix_bg_link")


@fix_bg_link.command("run")
def run(**kwargs):
    link = ""
    species = EtcDataSpeciesRegion.query.filter_by(country="BG", dataset_id=5)
    habitats = EtcDataHabitattypeRegion.query.filter_by(country="BG", dataset_id=5)
    # for specie in species:
    #     specie.filename = link
    #     db.session.add(specie)
    #     db.session.commit()

    for habitat in habitats:
        habitat.filename = link
        db.session.add(habitat)
        db.session.commit()
