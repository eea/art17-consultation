import click
import re

from flask.cli import AppGroup

from art17 import models

set_new_factsheets_urls = AppGroup("set_new_factsheets_urls")


def set_new_factsheets_urls_for_given_entity(model_cls, code_field):
    from art17 import models
    entities_2006 = model_cls.query.filter_by(dataset_id=1).all()
    print(f"Number of 2006 {model_cls.__name__}: {len(entities_2006)}")
    count = 0
    for entity in entities_2006:
        if entity.remote_url_2006:
            entity.remote_url_2006 = entity.remote_url_2006_new
            models.db.session.add(entity)
            print(
                f"{count} Updated remote_url_2006 for {model_cls.__name__}: {getattr(entity, code_field)}"
            )
        count += 1
    models.db.session.commit()
    print(f"Updated {model_cls.__name__} 2006")

    entities_2012 = model_cls.query.filter_by(dataset_id=3).all()
    print(f"Number of 2012 {model_cls.__name__}: {len(entities_2012)}")
    count = 0
    for entity in entities_2012:
        if entity.remote_url_2012:
            entity.remote_url_2012 = entity.remote_url_2012_new
            models.db.session.add(entity)
            print(
                f"{count} Updated remote_url_2012 for {model_cls.__name__}: {getattr(entity, code_field)}"
            )
        count += 1
    models.db.session.commit()
    print(f"Updated {model_cls.__name__} 2012")


@set_new_factsheets_urls.command("run")
def run(**kwargs):
    set_new_factsheets_urls_for_given_entity(models.EtcDataSpeciesRegion, "speciescode")
    set_new_factsheets_urls_for_given_entity(
        models.EtcDataHabitattypeRegion, "habitatcode"
    )
