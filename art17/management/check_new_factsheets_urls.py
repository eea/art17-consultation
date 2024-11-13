import click
import urllib

from time import sleep

from flask.cli import AppGroup
from flask import current_app as app

from art17 import models

check_new_factsheets_urls = AppGroup("check_new_factsheets_urls")


def check_urls(entity_name, model_cls, field):
    remote_urls = (
        model_cls.query.with_entities(getattr(model_cls, field)).distinct().all()
    )
    print(f"Number of remote_urls for {entity_name}: {len(remote_urls)}")
    count = 0
    for (remote_url,) in remote_urls:
        if not remote_url:
            count += 1
            print(f"{count} No remote_url for {entity_name}")
            continue
        sleep(0.1)
        base_remote_url = app.config.get("FACTSHEETS_REMOTE_URLS", "")
        pdf_url = f"{base_remote_url}{remote_url}"
        try:
            code = urllib.request.urlopen(pdf_url).getcode()
        except:
            count += 1
            print(f"{count} Error on {pdf_url}")
            continue
        if code == 200:
            print(f"{count} URL is OK for {pdf_url}")
        else:
            print(f"{count} Error on {pdf_url}")
        count += 1


@check_new_factsheets_urls.command("run")
@click.option("-f", "--field", type=click.Choice(["old", "new"]), required=True)
@click.option("-p", "--period", type=click.Choice(["2006", "2012"]), required=True)
@click.option(
    "-e", "--entity", type=click.Choice(["species", "habitat"]), required=True
)
def run(**kwargs):
    entity_name = "Species" if kwargs["entity"] == "species" else "Habitat"
    model_cls = (
        models.EtcDataSpeciesRegion
        if kwargs["entity"] == "species"
        else models.EtcDataHabitattypeRegion
    )
    field = "remote_url_2006" if kwargs["field"] == "old" else "remote_url_2006_new"
    check_urls(entity_name, model_cls, field)
