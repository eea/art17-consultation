import os.path

from flask import Blueprint, render_template, request, current_app as app
from flask.views import MethodView
from jinja2 import Markup

from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import db, Wiki, WikiChange

factsheet = Blueprint('factsheets', __name__)

PRIORITY_TEXT = {'0': 'No', '1': 'Yes', '2': 'Yes in Ireland'}
REASONS_MANUAL = {'n': 'Not genuine', 'y': 'Genuine', 'nc': 'No change'}
REASONS = {'a': 'Genuine', 'b': 'Better data', 'c': 'Change in methods',
           'e': 'Change in methods', 'n': 'No change', 'd': 'No data'}


@factsheet.app_template_global('inject_static_file')
def inject_static_file(filepath):
    data = None
    with open(os.path.join(app.static_folder, filepath), 'r') as f:
        data = f.read()
    return Markup(data)


@factsheet.app_template_global('get_percentage')
def get_percentage(total, value):
    if not total:
        return 0
    percentage = float(value or 0) / total * 100
    if 0 < percentage < 1:
        return round(percentage, 2)
    else:
        return int(round(percentage))


@factsheet.app_template_global('get_reason_for_change_manual')
def get_reason_for_change_manual(value):
    return REASONS_MANUAL.get(value, '')


@factsheet.app_template_global('get_reason_for_change')
def get_reason_for_change(value):
    if not value:
        return ''
    return REASONS.get(value[0], '')


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

    def get_objects(self, period, subject):
        return (self.model_cls.query
                .filter_by(dataset_id=period, subject=subject)
                .all())

    def get(self):
        period = request.args.get('period')
        subject = request.args.get('subject')
        self.set_assessment(period, subject)
        manual_objects = self.get_manual_objects(period, subject)
        total_range = sum([float(getattr(obj, self.range_field) or 0)
                           for obj in manual_objects])

        context = self.get_context()
        context.update({
            'group': self.get_group_for_subject(subject),
            'regions': self.get_regions(period, subject),
            'priority': self.get_priority(),
            'wiki': self.get_wiki(period, subject),
            'manual_objects': manual_objects,
            'total_range': total_range,
            'objects': self.get_objects(period, subject),
        })
        return render_template(self.template_name, **context)


class SpeciesFactSheet(FactSheet, SpeciesMixin):
    template_name = 'factsheet/species.html'
    range_field = 'range_surface_area'

    def get_context(self):
        return {
            'name': self.assessment.subject,
            'annexes': self.get_annexes(),
        }

    def get_annexes(self):
        annexes = list(
            self.model_cls.query
            .filter_by(subject=self.assessment.subject,
                       dataset_id=self.assessment.dataset_id)
            .with_entities('annex_II', 'annex_IV', 'annex_V')
            .distinct()
            .first()
        )
        return ', '.join(filter(bool, annexes))


class HabitatFactSheet(FactSheet, HabitatMixin):
    template_name = 'factsheet/habitat.html'
    range_field = 'coverage_surface_area'

    def get_context(self):
        return {
            'name': self.assessment.habitat.name,
            'code': self.assessment.code,
        }


factsheet.add_url_rule('/species/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-species'))
factsheet.add_url_rule('/habitat/factsheet/',
                       view_func=HabitatFactSheet.as_view('factsheet-habitat'))