import click
import re
from flask.cli import AppGroup

from art17 import models

generate_new_factsheets_urls = AppGroup("generate_new_factsheets_urls")


def get_new_link(old_link):
    dir_regex = r"[^/]+/download/en/1/"
    dir_name = re.search(dir_regex, old_link).group(0)
    return old_link.replace("library/", "").replace(dir_name, "")


@generate_new_factsheets_urls.command("run")
@click.option(
    "-e", "--entity", type=click.Choice(["species", "habitat"]), required=True
)
def run(**kwargs):
    model_cls = (
        models.EtcDataSpeciesRegion
        if kwargs["entity"] == "species"
        else models.EtcDataHabitattypeRegion
    )
    code_attr = "speciescode" if kwargs["entity"] == "species" else "habitatcode"
    entities_2006 = model_cls.query.filter_by(dataset_id=1).all()
    print(f"Number of entities 2006: {len(entities_2006)}")
    for entity in entities_2006:
        if entity.remote_url_2006:
            entity.remote_url_2006_new = get_new_link(entity.remote_url_2006)
            models.db.session.add(entity)
        else:
            print(
                f"No remote_url_2006 for {model_cls.__name__}: {getattr(entity, code_attr)}"
            )
    models.db.session.commit()
    print(f"Updated entities 2006 for {kwargs['entity']}")

    entities_2012 = model_cls.query.filter_by(dataset_id=3).all()
    print(f"Number of entities 2012: {len(entities_2012)}")
    for entity in entities_2012:
        if entity.remote_url_2012:
            entity.remote_url_2012_new = get_new_link(entity.remote_url_2012)
            models.db.session.add(entity)
        else:
            print(
                f"No remote_url_2012 for {model_cls.__name__}: {getattr(entity, code_attr)}"
            )
    models.db.session.commit()
    print(f"Updated entities 2012 for {kwargs['entity']}")
