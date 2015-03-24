from flask import Blueprint, render_template, request
from flask.views import MethodView

from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import db, Wiki, WikiChange

factsheet = Blueprint('factsheets', __name__)

PRIORITY_TEXT = {'0': 'No', '1': 'Yes', '2': 'Yes in Ireland'}


class FactSheet(MethodView):

    def set_assessment(self, period, subject):
        self.assessment = (self.model_cls.query
                           .filter_by(subject=subject, dataset_id=period)
                           .first_or_404())

    def get_regions(self, period, subject):
        regions = (
            self.model_manual_cls.query
            .filter_by(subject=subject, dataset_id=period, decision='OK')
            .with_entities(self.model_manual_cls.region)
            .distinct().all())
        return ', '.join(['CONT' if r[0] == 'CON' else r[0] for r in regions])

    def get_priority(self):
        return PRIORITY_TEXT.get(self.assessment.priority, 'Unknown')

    def get_wiki(self, period, subject):
        wiki = (db.session.query(WikiChange)
                .join(Wiki)
                .filter(Wiki.dataset_id == period,
                        getattr(Wiki, self.wiki_subject_column) == subject,
                        Wiki.region_code == '',
                        WikiChange.active == 1)
                .first())
        return wiki.body if wiki else ''

    def get(self):
        period = request.args.get('period')
        subject = request.args.get('subject')
        self.set_assessment(period, subject)

        context = {
            'name': self.get_name(),
            'group': self.get_group_for_subject(subject),
            'regions': self.get_regions(period, subject),
            'code': self.assessment.code,
            'priority': self.get_priority(),
            'wiki': self.get_wiki(period, subject),
        }
        return render_template(self.template_name, **context)


class SpeciesFactSheet(FactSheet, SpeciesMixin):
    template_name = 'factsheet/species.html'

    def get_name(self):
        return self.assessment.subject


class HabitatFactSheet(FactSheet, HabitatMixin):
    template_name = 'factsheet/habitat.html'

    def get_name(self):
        return self.assessment.habitat.name


factsheet.add_url_rule('/species/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-species'))
factsheet.add_url_rule('/habitat/factsheet/',
                       view_func=HabitatFactSheet.as_view('factsheet-habitat'))
