from collections import OrderedDict

from flask import Blueprint, render_template, request, current_app as app
from flask.ext.script import Manager
from flask.views import MethodView

from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import db, Wiki, WikiChange
from art17.pdf import PdfRenderer
from art17.queries import THREATS_QUERY, COVERAGE_QUERY

factsheet = Blueprint('factsheets', __name__)
factsheet_manager = Manager()

PRIORITY_TEXT = {'0': 'No', '1': 'Yes', '2': 'Yes in Ireland'}
REASONS_MANUAL = {'n': 'Not genuine', 'y': 'Genuine', 'nc': 'No change'}
REASONS = {'a': 'Genuine', 'b': 'Better data', 'c': 'Change in methods',
           'e': 'Change in methods', 'n': 'No change', 'd': 'No data'}


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


@factsheet.app_template_global('format_regions')
def format_regions(regions):
    return ', '.join(['CONT' if r == 'CON' else r for r in regions])


class FactSheet(MethodView):
    def get_regions(self, period, subject):
        regions = (
            self.model_manual_cls.query
            .filter_by(subject=subject, dataset_id=period, decision='OK')
            .with_entities(self.model_manual_cls.region)
            .distinct().all()
        )
        return [region[0] for region in regions]

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

    def get_pressures(self, subject, pressure_type):
        if not self.engine:
            return []
        result = self.engine.execute(THREATS_QUERY.format(
            subject=subject,
            pressure_type=pressure_type,
            checklist_table=self.checklist_table,
            regions_MS_table=self.regions_MS_table,
            join_column=self.join_column,
            regionhash_column=self.regionhash_column,
            subject_column=self.subject_column,
        ))
        return [dict(row.items()) for row in result]

    def get_coverage(self, subject):
        if not self.engine:
            return []
        result = self.engine.execute(COVERAGE_QUERY.format(subject=subject))
        coverage = OrderedDict()
        for row in result:
            coverage.setdefault(row['country'], {})[row['region']] = row['pc']
        return coverage

    def get_context_data(self, **kwargs):
        period = kwargs.get('period')[0]
        subject = kwargs.get('subject')[0]
        manual_objects = self.get_manual_objects(period, subject)
        total_range = sum([float(getattr(obj, self.range_field) or 0)
                           for obj in manual_objects])

        self.assessment = (self.model_cls.query
                           .filter_by(subject=subject, dataset_id=period)
                           .first_or_404())
        self.engine = (
            db.get_engine(app, 'factsheet') if app.config['SQLALCHEMY_BINDS']
            and app.config['SQLALCHEMY_BINDS'].get('factsheet') else None)

        return {
            'group': self.get_group_for_subject(subject),
            'regions': self.get_regions(period, subject),
            'priority': self.get_priority(),
            'wiki': self.get_wiki(period, subject),
            'manual_objects': manual_objects,
            'total_range': total_range,
            'objects': self.get_objects(period, subject),
            'pressures': self.get_pressures(subject, 'p'),
            'threats': self.get_pressures(subject, 't'),
            'coverage': self.get_coverage(subject),
        }

    def get(self):
        context = self.get_context_data(**request.args)
        return render_template(self.template_name, **context)

    def get_pdf(self, **kwargs):
        context = self.get_context_data(**kwargs)
        title = context.get('name', '(untitled)')
        return PdfRenderer(self.template_name,
                           title=title,
                           height='11.693in', width='8.268in',
                           context=context)


class SpeciesFactSheet(FactSheet, SpeciesMixin):
    template_name = 'factsheet/species.html'
    range_field = 'range_surface_area'
    checklist_table = 'data_species_check_list'
    regions_MS_table = 'data_species_regions_MS_level'
    subject_column = 'assessment_speciesname'
    join_column = 'speciesname'
    regionhash_column = 'species_regionhash'

    def get_context_data(self, **kwargs):
        context = super(SpeciesFactSheet, self).get_context_data(**kwargs)
        context.update({
            'name': self.assessment.subject,
            'annexes': self.get_annexes(),
        })
        return context

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
    checklist_table = 'data_habitats_check_list'
    regions_MS_table = 'data_habitats_regions_MS_level'
    subject_column = join_column = 'habitatcode'
    regionhash_column = 'habitat_regionhash'

    def get_context_data(self, **kwargs):
        context = super(HabitatFactSheet, self).get_context_data(**kwargs)
        context.update({
            'name': self.assessment.habitat.name,
            'code': self.assessment.code,
        })
        return context


factsheet.add_url_rule('/species/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-species'))
factsheet.add_url_rule('/habitat/factsheet/',
                       view_func=HabitatFactSheet.as_view('factsheet-habitat'))


def _get_pdf(subject, period, view_cls):
    view = view_cls()
    renderer = view.get_pdf(subject=subject, period=period)
    renderer._generate()
    print("Generated: " + renderer.pdf_path)


@factsheet_manager.command
def species(subject, period):
    return _get_pdf(subject, period, SpeciesFactSheet)


@factsheet_manager.command
def habitat(subject, period):
    return _get_pdf(subject, period, HabitatFactSheet)
