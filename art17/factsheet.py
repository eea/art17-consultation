from collections import OrderedDict
import urllib
import os.path
from path import path

from sqlalchemy import and_
from sqlalchemy.sql import func, or_
from flask import (
    Blueprint, render_template, request, current_app as app, url_for,
)
from flask.ext.script import Manager
from flask.views import MethodView

from art17.common import admin_perm
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import db, Wiki, WikiChange, Dataset
from art17.pdf import PdfRenderer
from art17.queries import (
    THREATS_QUERY, COVERAGE_QUERY_SPECIES, COVERAGE_QUERY_HABITAT,
    MEASURES_QUERY, N2K_QUERY, ANNEX_QUERY
)
from art17.utils import slugify

factsheet = Blueprint('factsheet', __name__)
factsheet_manager = Manager()

PRIORITY_TEXT = {'0': 'No', '1': 'Yes', '2': 'Yes in Ireland'}
REASONS_MANUAL = {'n': 'Not genuine', 'y': 'Genuine', 'nc': ''}
REASONS = {'a': 'Genuine', 'b': 'Better data', 'c': 'Change in methods',
           'e': 'Change in methods', 'n': '', 'd': 'No data'}


def get_arg(kwargs, key, default=None):
    arg = kwargs.get(key)
    return arg[0] if isinstance(arg, list) else arg or default


def _fix_p(text):
    return text.replace('<p>&nbsp;</p>', '')


@factsheet.app_template_global('get_percentage')
def get_percentage(total, value):
    if not total:
        return 0
    percentage = (value or 0) / total * 100
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


@factsheet.app_template_global('get_conclusion_assessment_prev_colour')
def get_conclusion_assessment_prev_colour(obj):
    if obj.eu_country_code in ('BG', 'RO'):
        return None

    if not obj.conclusion_assessment_prev:
        return 'NA'

    return obj.conclusion_assessment_prev[0:2]


@factsheet.app_template_global('get_maps_url')
def get_maps_url(which, type, code):
    maps_format = app.config['MAPS_FORMAT']
    filename = maps_format.format(which=which, type=type, code=code)
    maps_path = path(app.static_folder) / app.config['MAPS_STATIC'] / filename
    if maps_path.exists():
        return path(app.config['MAPS_STATIC']) / filename
    else:
        return 'img/blank_map0{which}.png'.format(which=which)


class FactSheet(MethodView):
    def get_regions(self, period, subject):
        regions = super(FactSheet, self).get_regions(period, subject)[1:]
        return [name for abbr, name in regions]

    def get_region_codes(self, period, subject):
        regions = super(FactSheet, self).get_regions(period, subject)[1:]
        return [abbr for abbr, name in regions]

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
        return _fix_p(wiki.body if wiki else '')

    def get_manual_objects(self, period, subject):
        return (
            db.session.query(
                self.model_manual_cls,
                func.sum(self.model_cls.distribution_grid_area))
            .join(self.model_cls, and_(
                self.model_manual_cls.subject == self.model_cls.subject,
                self.model_manual_cls.dataset_id == self.model_cls.dataset_id,
                self.model_manual_cls.region == self.model_cls.region))
            .filter(
                self.model_manual_cls.subject == subject,
                self.model_manual_cls.dataset_id == period,
                self.model_manual_cls.decision == 'OK')
            .group_by(self.model_manual_cls.region))

    def get_objects(self, period, subject):
        return (self.model_cls.query
                .filter_by(dataset_id=period, subject=subject)
                .order_by(self.model_cls.region,
                          self.model_cls.eu_country_code))

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
            return {}
        result = self.engine.execute(
            self.coverage_query.format(subject=subject,
                                       join_column=self.join_column,
                                       subject_column=self.subject_column))
        coverage = OrderedDict()
        regions = []
        for row in result:
            coverage.setdefault(row['country'], {})[row['region']] = row['pc']
            if row['region'] not in regions:
                regions.append(row['region'])
        regions.sort()
        return coverage, regions

    def get_measures(self, subject):
        if not self.engine:
            return {}
        return self.engine.execute(MEASURES_QUERY.format(
            subject=subject,
            checklist_table=self.checklist_table,
            regions_MS_table=self.regions_MS_table,
            join_column=self.join_column,
            regionhash_column=self.regionhash_column,
            subject_column=self.subject_column,
            extra=self.extra_condition,
        ))

    def get_url(self, subject, period):
        base_url = url_for(self.summary_view, _external=True)
        params = {'subject': subject,
                  'period': period,
                  'region': '',
                  'group': self.assessment.group}
        return '?'.join((base_url, urllib.urlencode(params)))

    def get_countries(self, subject, period):
        return [country for country, in (
            self.model_cls.query
            .with_entities(self.model_cls.eu_country_code)
            .filter(self.model_cls.subject == subject,
                    self.model_cls.dataset_id == period,
                    self.model_cls.distribution_grid_area == None)
            .distinct()
            .all())]

    def get_context_data(self, **kwargs):
        period = (
            get_arg(kwargs, 'period', None) or
            app.config['FACTSHEET_DEFAULT_PERIOD']
        )
        subject = get_arg(kwargs, 'subject')
        manual_objects = self.get_manual_objects(period, subject)
        total_area = sum([obj[1] or 0 for obj in manual_objects])

        self.assessment = (self.model_cls.query
                           .filter_by(subject=subject, dataset_id=period)
                           .first_or_404())
        self.engine = (
            db.get_engine(app, 'factsheet') if app.config['SQLALCHEMY_BINDS']
            and app.config['SQLALCHEMY_BINDS'].get('factsheet') else None)
        coverage, regions = self.get_coverage(subject)

        return {
            'group': self.get_group_for_subject(subject),
            'regions': self.get_regions(period, subject),
            'region_codes': regions,
            'priority': self.get_priority(),
            'wiki': self.get_wiki(period, subject),
            'manual_objects': manual_objects,
            'total_area': total_area,
            'objects': self.get_objects(period, subject),
            'pressures': self.get_pressures(subject, 'p'),
            'threats': self.get_pressures(subject, 't'),
            'coverage': coverage,
            'measures': self.get_measures(subject),
            'url': self.get_url(subject, period),
            'countries': self.get_countries(subject, period),
            'period': Dataset.query.get_or_404(period).name,
            'assessment': self.assessment,
        }

    def get_all(self):
        period = request.args.get('period',
                                  app.config['FACTSHEET_DEFAULT_PERIOD'])
        return (
            self.model_cls.query
            .filter_by(dataset_id=period)
            .group_by(getattr(self.model_cls, 'subject'))
        )

    def list_all(self):
        objects = self.get_all()
        return render_template('factsheet/list_all.html', objects=objects,
                               subject=self.subject_name,
                               url_base=self.url_base)

    def get(self):
        admin_perm.test()
        if not request.args.get('subject'):
            return self.list_all()
        context = self.get_context_data(**request.args)
        return render_template(self.template_name, **context)

    def get_pdf(self, **kwargs):
        context = self.get_context_data(**kwargs)
        title = context.get('name', '(untitled)')
        pdf_file = self._get_pdf_file_name()
        footer_url = url_for('factsheet.factsheet-footer', _external=True)
        base_header_url = url_for(self.header_endpoint, _external=True)
        params = {'subject': self.assessment.subject,
                  'period': self.assessment.dataset_id}
        header_url = '?'.join((base_header_url, urllib.urlencode(params)))

        return PdfRenderer(self.template_name, pdf_file=pdf_file,
                           title=title,
                           height='11.693in', width='8.268in',
                           context=context,
                           header_url=header_url,
                           footer_url=footer_url)


class SpeciesFactSheet(FactSheet, SpeciesMixin):
    template_name = 'factsheet/species.html'
    range_field = 'range_surface_area'
    checklist_table = 'data_species_check_list'
    regions_MS_table = 'data_species_regions_MS_level'
    subject_column = 'assessment_speciesname'
    join_column = 'speciesname'
    regionhash_column = 'species_regionhash'
    coverage_query = COVERAGE_QUERY_SPECIES
    summary_view = 'summary.species-summary'
    extra_condition = "AND UPPER(RS3.annex_II) like 'Y%%'"
    url_base = '.factsheet-species'
    header_endpoint = 'factsheet.species-header'

    @classmethod
    def get_pdf_file_name(cls, assessment):
        file_name = '{0}/{1}'.format(slugify(assessment.group),
                                     slugify(assessment.subject))
        return file_name

    def _get_pdf_file_name(self):
        return self.get_pdf_file_name(self.assessment)

    def get_has_n2k(self):
        if not self.engine:
            return True
        result = self.engine.execute(
            N2K_QUERY.format(subject=self.assessment.subject)
        )
        row = result and result.first()
        return row and row['cond'] > 0

    def get_context_data(self, **kwargs):
        context = super(SpeciesFactSheet, self).get_context_data(**kwargs)
        context.update({
            'name': self.assessment.subject,
            'annexes': self.get_annexes(),
            'has_n2k': self.get_has_n2k(),
        })
        return context

    def get_annexes(self):
        if not self.engine:
            return ''
        result = self.engine.execute(
            ANNEX_QUERY.format(subject=self.assessment.subject)
        )
        row = result and result.first() or ''
        return ', '.join(filter(bool, row))

    def get_manual_objects(self, period, subject):
        q = super(SpeciesFactSheet, self).get_manual_objects(period, subject)
        return q.filter(or_(
            self.model_cls.species_type == None,
            ~self.model_cls.species_type.in_(['IRM', 'OP', 'PEX'])))

    def get_objects(self, period, subject):
        q = super(SpeciesFactSheet, self).get_objects(period, subject)
        return q.filter(or_(
            self.model_cls.species_type == None,
            ~self.model_cls.species_type.in_(['IRM', 'OP', 'PEX'])))


class HabitatFactSheet(FactSheet, HabitatMixin):
    template_name = 'factsheet/habitat.html'
    range_field = 'coverage_surface_area'
    checklist_table = 'data_habitats_check_list'
    regions_MS_table = 'data_habitats_regions_MS_level'
    subject_column = join_column = 'habitatcode'
    regionhash_column = 'habitat_regionhash'
    coverage_query = COVERAGE_QUERY_HABITAT
    summary_view = 'summary.habitat-summary'
    extra_condition = ''
    url_base = '.factsheet-habitat'
    header_endpoint = 'factsheet.habitat-header'


    @classmethod
    def get_pdf_file_name(cls, assessment):
        name = (
            (assessment.lu_factsheets and
             assessment.lu_factsheets.nameheader)
            or assessment.subject
        )
        file_name = u'{0}-{1}'.format(assessment.code, name)
        return slugify(file_name)

    def _get_pdf_file_name(self):
        return self.get_pdf_file_name(self.assessment)

    def get_context_data(self, **kwargs):
        context = super(HabitatFactSheet, self).get_context_data(**kwargs)
        context.update({
            'name': self.assessment.habitat.name,
            'code': self.assessment.code,
            'has_n2k': True,  # Apparently, they all have
        })
        return context

    def get_manual_objects(self, period, subject):
        q = super(HabitatFactSheet, self).get_manual_objects(period, subject)
        return q.filter(self.model_cls.habitattype_type_asses == 1)


class FactSheetHeader(MethodView):
    def get_context_data(self, **kwargs):
        subject = get_arg(kwargs, 'subject')
        period = get_arg(kwargs, 'period')

        self.assessment = (self.model_cls.query
                           .filter_by(subject=subject, dataset_id=period)
                           .first_or_404())
        label = self.subject_name.capitalize()
        return {'period': self.assessment.dataset.name,
                'subject': subject,
                'label': label, }

    def get(self):
        context = self.get_context_data(**request.args)
        return render_template('factsheet/common/header.html', **context)


class SpeciesHeader(SpeciesMixin, FactSheetHeader):
    def get_context_data(self, **kwargs):
        context = super(SpeciesHeader, self).get_context_data(**kwargs)
        context['subject'] = u'<em>{}</em>'.format(context['subject'])
        return context


class HabitatHeader(HabitatMixin, FactSheetHeader):
    def get_context_data(self, **kwargs):
        context = super(HabitatHeader, self).get_context_data(**kwargs)
        context['subject'] = u'{} <em>{}</em>'.format(
            context['subject'],
            self.assessment.lu_factsheets.nameheader
        )
        return context


class FactSheetFooter(MethodView):
    def get(self):
        return render_template('factsheet/common/footer.html')


factsheet.add_url_rule('/species/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-species'))
factsheet.add_url_rule('/habitat/factsheet/',
                       view_func=HabitatFactSheet.as_view('factsheet-habitat'))
factsheet.add_url_rule('/factsheet/footer/',
                       view_func=FactSheetFooter.as_view('factsheet-footer'))
factsheet.add_url_rule('/species/factsheet/header/',
                       view_func=SpeciesHeader.as_view('species-header'))
factsheet.add_url_rule('/habitat/factsheet/header/',
                       view_func=HabitatHeader.as_view('habitat-header'))


def generate_factsheet_url(category, subject, period):
    if category == 'species':
        model_cls = SpeciesMixin.model_cls
        fs_cls = SpeciesFactSheet
    elif category == 'habitat':
        model_cls = HabitatMixin.model_cls
        fs_cls = HabitatFactSheet
    else:
        raise NotImplementedError('Unknown category:', category)

    period = period or app.config['FACTSHEET_DEFAULT_PERIOD']
    assessment = (
        model_cls.query.filter_by(subject=subject,
                                  dataset_id=period).first()
    )
    if not assessment:
        return None
    pdf_path = str(
        path(app.config['PDF_DESTINATION'] )
        / fs_cls.get_pdf_file_name(assessment)
    ) + '.pdf'
    real_path = str(path(app.static_folder) / pdf_path)
    if os.path.exists(real_path):
        return url_for('static', filename=pdf_path)
    return None


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


@factsheet_manager.command
def genall(period):
    map = {SpeciesFactSheet: species, HabitatFactSheet: habitat}
    for view_cls, command in map.items():
        view = view_cls()
        for o in view.get_all():
            command(o.subject, period)
    print("Done")
