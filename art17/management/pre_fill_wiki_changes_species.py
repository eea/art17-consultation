import csv

from flask_script import Manager, Option
from flask_security.script import Command
from flask_sqlalchemy import SQLAlchemy

from art17.models import db, Wiki, WikiChange


class PreFillWikiChangesSpecies(Command):

    option_list = Command.option_list + (
        Option('-d', '--dataset', dest='dataset_id', required=True),
        Option('-f', '--file', dest='file', required=True),
    )

    def run(self, **kwargs):
        with open(kwargs['file']) as file:
            rows = [{k: v for k, v in row.items()} for row in 
                    csv.DictReader(file, skipinitialspace=True)]
            for row in rows:
                wiki =Wiki.query.filter_by(
                       region_code=row['region'],
                       assesment_speciesname=row['2019assessment_speciesname'],
                       dataset_id=kwargs['dataset_id']
                ).all()
                if not wiki:
                    wiki_new = Wiki(
                        dataset_id=kwargs['dataset_id'],
                        region_code=row['region'],
                        assesment_speciesname=row['2019assessment_speciesname'])
                    db.session.add(wiki_new)
                    db.session.commit()
                    wiki_change_new = WikiChange(
                        wiki_id=wiki_new.id,
                        body=row['body'],
                        editor='admin',
                        revised=False,
                        active=True,
                        dataset_id=kwargs['dataset_id']
                    )
                    db.session.add(wiki_change_new)
                    db.session.commit()


pre_fill_wiki_changes_species = Manager()
pre_fill_wiki_changes_species.add_command('run', PreFillWikiChangesSpecies())