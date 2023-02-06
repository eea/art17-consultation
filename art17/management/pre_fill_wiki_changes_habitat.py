import click
from flask.cli import AppGroup

from art17.models import Wiki, WikiChange, db

pre_fill_wiki_changes_habitat = AppGroup("pre_fill_wiki_changes_habitat")


@pre_fill_wiki_changes_habitat.command("run")
@click.option("-d", "--dataset", "dataset_id")
@click.option("-fd", "--from-dataset", "from_dataset_id")
def run(**kwargs):
    wikis = Wiki.query.filter_by(dataset_id=kwargs["from_dataset_id"]).filter(
        Wiki.habitatcode.isnot(None)
    )
    for wiki in wikis:
        exists = Wiki.query.filter_by(
            dataset_id=kwargs["dataset_id"],
            region_code=wiki.region_code,
            assesment_speciesname=wiki.assesment_speciesname,
            habitatcode=wiki.habitatcode,
        ).all()
        if not exists:
            wiki_new = Wiki(
                dataset_id=kwargs["dataset_id"],
                region_code=wiki.region_code,
                assesment_speciesname=wiki.assesment_speciesname,
                habitatcode=wiki.habitatcode,
            )
            db.session.add(wiki_new)
            db.session.commit()
            wiki_change = wiki.changes.filter_by(active=True).first()
            wiki_change_new = WikiChange(
                wiki_id=wiki_new.id,
                body=wiki_change.body,
                editor="admin",
                revised=False,
                active=True,
                dataset_id=kwargs["dataset_id"],
            )
            db.session.add(wiki_change_new)
            db.session.commit()
