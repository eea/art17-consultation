from flask_script import Manager, Option
from flask_security.script import Command
from flask_sqlalchemy import SQLAlchemy

from art17.models import db, Wiki, WikiChange


class PreFillWikiChangesHabitat(Command):

    option_list = Command.option_list + (
        Option('-d', '--dataset', dest='dataset_id', required=True),
        Option('-fd', '--from-dataset', dest="from_dataset_id", required=True)
    )

    def run(self, **kwargs):
        wikis =Wiki.query.filter_by(dataset_id=kwargs['from_dataset_id']).filter(Wiki.habitatcode.isnot(None))
        for wiki in wikis:
            exists = Wiki.query.filter_by(
                dataset_id=kwargs['dataset_id'],
                region_code=wiki.region_code,
                assesment_speciesname=wiki.assesment_speciesname,
                habitatcode=wiki.habitatcode
            ).all()
            if not exists:
                wiki_new = Wiki(
                    dataset_id=kwargs['dataset_id'],
                    region_code=wiki.region_code,
                    assesment_speciesname=wiki.assesment_speciesname,
                    habitatcode=wiki.habitatcode
                )
                db.session.add(wiki_new)
                db.session.commit()
                wiki_change = wiki.changes.filter_by(active=True).first()
                wiki_change_new = WikiChange(
                    wiki_id=wiki_new.id,
                    body=wiki_change.body,
                    editor='admin',
                    revised=False,
                    active=True,
                    dataset_id=kwargs['dataset_id']
                )
                db.session.add(wiki_change_new)
                db.session.commit()



pre_fill_wiki_changes_habitat = Manager()
pre_fill_wiki_changes_habitat.add_command('run', PreFillWikiChangesHabitat())