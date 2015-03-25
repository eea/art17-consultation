from flask import Blueprint, render_template, request
from flask.views import MethodView

from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import db, Wiki, WikiChange

factsheet = Blueprint('factsheets', __name__)

PRIORITY_TEXT = {'0': 'No', '1': 'Yes', '2': 'Yes in Ireland'}
REASONS_MAPPING = {'n': 'Not genuine', 'y': 'Genuine', 'nc': 'No change'}


@factsheet.app_template_global('get_percentage')
def get_percentage(row, manual_objects, field):
    total = sum([float(getattr(obj, field) or 0) for obj in manual_objects])
    if not total:
        return 0
    percentage = float(getattr(row, field) or 0) / total * 100
    if 0 < percentage < 1:
        return round(percentage, 2)
    else:
        return int(round(percentage))

@factsheet.app_template_global('get_reason_for_change')
def get_reason_for_change(row):
    return REASONS_MAPPING.get(row.conclusion_assessment_change, 'Unknown')


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

    def get_manual_objects(self, period, subject):
        return (self.model_manual_cls.query
                .filter_by(dataset_id=period, subject=subject, decision='OK')
                .all())

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
            'manual_objects': self.get_manual_objects(period, subject),
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
