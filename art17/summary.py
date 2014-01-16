from flask import (
    Blueprint,
    views,
    request,
    render_template,
    jsonify,
    url_for,
)

from art17.models import (
    EtcDicBiogeoreg,
    EtcDataSpeciesRegion,
    EtcQaErrorsSpeciesManualChecked,
    Dataset,
    db,
    t_restricted_species,
    EtcDataHabitattypeRegion,
    EtcQaErrorsHabitattypeManualChecked,
    EtcDicMethod,
)

from art17.mixins import SpeciesMixin, HabitatMixin

from art17.common import (
    get_default_period,
    admin_perm,
    expert_perm,
    population_size_unit,
    population_ref,
    CONCLUSION_CLASSES,
    COUNTRY_ASSESSMENTS,
    QUALITIES,
)
from art17.forms import SummaryFilterForm
from art17.utils import str2num


summary = Blueprint('summary', __name__)


@summary.route('/')
def homepage():
    return render_template('homepage.html')


@summary.app_template_global('can_view')
def can_view(record, countries):
    return (admin_perm().can() or expert_perm().can() or
            record.eu_country_code not in countries)


@summary.app_context_processor
def inject_fuctions():
    return {
        'record_errors': record_errors,
        'parse_qa_errors': parse_qa_errors,
        'population_size_unit': population_size_unit,
        'population_ref': population_ref,
    }


@summary.app_context_processor
def inject_static():
    return {
        'CONCLUSION_CLASSES': CONCLUSION_CLASSES,
        'COUNTRY_ASSESSMENTS': COUNTRY_ASSESSMENTS,
        'QUALITIES': QUALITIES,
        'ASSESSMENT_DETAILS': dict(
            db.session.query(EtcDicMethod.method, EtcDicMethod.details)
        ),
    }


@summary.app_template_filter('str2num')
def _str2num(value, default='N/A'):
    return str2num(value, default=default)


@summary.app_template_filter('get_quality')
def get_quality(value, default='N/A'):
    if value and value[0] in QUALITIES:
        return value[0]
    return default


def record_errors(record):
    if isinstance(record, EtcDataSpeciesRegion):
        qs = EtcQaErrorsSpeciesManualChecked.query.filter_by(
            assesment_speciesname=record.assesment_speciesname,
            region=record.region,
            eu_country_code=record.eu_country_code,
        )
    elif isinstance(record, EtcDataHabitattypeRegion):
        qs = EtcQaErrorsHabitattypeManualChecked.query.filter_by(
            habitatcode=record.code,
            region=record.region,
            eu_country_code=record.eu_country_code,
        )
    else:
        raise ValueError("Invalid record type" + str(type(record)))
    return {
        e.field: {'text': e.text, 'suspect_value': e.suspect_value}
        for e in qs
    }


def format_error(error, record, field):
    if field in ('range_surface_area',
                 'complementary_favourable_range',
                 'complementary_favourable_range_q',
                 'range_yearly_magnitude',
                 'conclusion_range',
                 'percentage_range_surface_area',
                 'population_minimum_size',
                 'population_maximum_size',
                 'filled_population',
                 'population_size_unit',
                 'conclusion_population',
                 'percentage_population_mean_size',
                 'population_yearly_magnitude',
                 'complementary_favourable_population_q',
                 'complementary_favourable_population',
                 'filled_complementary_favourable_population',
                 'habitat_surface_area',
                 'conclusion_habitat',
                 'percentage_habitat_surface_area',
                 'habitat_trend',
                 'complementary_suitable_habitat'
                 ):
        return '%s: %s' % (error['text'], error['suspect_value'])
    return error['text']


def parse_qa_errors(fields, record, qa_errors):
    title = []
    classes = []
    if isinstance(fields, str):
        fields = [fields]
    for field in fields:
        if field in qa_errors:
            title.append(format_error(qa_errors[field], record, field))
            classes.append('qa_error')
    return '<br/>'.join(title), ' '.join(classes)


class Summary(views.View):

    def get_context(self):
        return {}

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        subject = request.args.get('subject')
        group = request.args.get('group')
        region = request.args.get('region')
        self.objects = []
        self.restricted_countries = []
        self.auto_objects = []
        self.setup_objects_and_data(period, subject, region)

        summary_filter_form = SummaryFilterForm(request.args)
        summary_filter_form.group.choices = self.get_groups(period)
        summary_filter_form.subject.choices = self.get_subjects(period, group)
        summary_filter_form.region.choices = self.get_regions(period, subject)

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''

        current_selection = self.get_current_selection(
            period_name, group, subject, region)
        annexes = self.get_annexes(subject)
        context = self.get_context()
        context.update({
            'objects': self.objects,
            'auto_objects': self.auto_objects,
            'restricted_countries': self.restricted_countries,
            'regions': EtcDicBiogeoreg.query.all(),
            'summary_filter_form': summary_filter_form,
            'current_selection': current_selection,
            'annexes': annexes,
            'group': group,
            'period_name': period_name,
        })

        return render_template(self.template_name, **context)

    def get_current_selection(self, period_name, group, species, region):
        if not group and not species:
            return []
        current_selection = [period_name, group, species]
        if region:
            region_name = EtcDicBiogeoreg.get_region_name(region)
            if region_name:
                current_selection.append(region_name[0])
        else:
            current_selection.append('All bioregions')
        return current_selection

    def get_annexes(self, species):
        annexes_results = (
            EtcDataSpeciesRegion.query
            .with_entities('annex_II', 'annex_IV', 'annex_V', 'priority')
            .filter(EtcDataSpeciesRegion.assesment_speciesname == species)
            .distinct()
            .first()
        )
        if not annexes_results:
            return []
        annexes = list(annexes_results)
        try:
            priority = int(annexes.pop())
        except ValueError:
            priority = 0
        if annexes[0] and priority:
            annexes[0] += '*'
        return filter(bool, annexes)


class SpeciesSummary(Summary, SpeciesMixin):

    template_name = 'species_summary.html'

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}
        if subject:
            filter_args['assesment_speciesname'] = subject
        else:
            return False
        self.restricted_countries = [r[0] for r in db.session.query(
            t_restricted_species.c.eu_country_code).
            filter(t_restricted_species.c.assesment_speciesname ==
                   subject.lower()).
            filter(t_restricted_species.c.show_data == 0).all()]
        if region:
            filter_args['region'] = region
        if filter_args:
            filter_args['dataset_id'] = period
            self.objects = self.model_cls.query.filter_by(**filter_args)
            self.auto_objects = self.model_auto_cls.query.filter_by(
                **filter_args
            )
        return True

    def get_context(self):
        return {
            'groups_url': url_for('.species-summary-groups'),
            'subjects_url': url_for('.species-summary-species'),
            'regions_url': url_for('.species-summary-regions'),
        }


class HabitatSummary(Summary, HabitatMixin):

    template_name = 'habitat_summary.html'

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}

        if subject:
            filter_args['code'] = subject
        else:
            return False
        if region:
            filter_args['region'] = region
        if filter_args:
            filter_args['dataset_id'] = period
            self.objects = self.model_cls.query.filter_by(**filter_args)
        return True

    def get_context(self):
        return {
            'groups_url': url_for('.habitat-summary-groups'),
            'subjects_url': url_for('.habitat-summary-species'),
            'regions_url': url_for('.habitat-summary-regions'),
        }


@summary.route('/species/summary/groups', endpoint='species-summary-groups')
def _groups():
    data = SpeciesMixin.get_groups(request.args['period'])
    return jsonify(data)


@summary.route('/species/summary/species', endpoint='species-summary-species')
def _species():
    period, group = request.args['period'], request.args['group']
    data = SpeciesMixin.get_subjects(period, group)
    return jsonify(data)


@summary.route('/species/summary/regions', endpoint='species-summary-regions')
def _regions():
    period, subject = request.args['period'], request.args['subject']
    data = SpeciesMixin.get_regions(period, subject)
    return jsonify(data)


@summary.route('/habitat/summary/groups', endpoint='habitat-summary-groups')
def _groups_habitat():
    data = HabitatMixin.get_groups(request.args['period'])
    return jsonify(data)


@summary.route('/habitat/summary/habitat', endpoint='habitat-summary-species')
def _species_habitat():
    period, group = request.args['period'], request.args['group']
    data = HabitatMixin.get_subjects(period, group)
    return jsonify(data)


@summary.route('/habitat/summary/regions', endpoint='habitat-summary-regions')
def _regions_habitat():
    period, subject = request.args['period'], request.args['subject']
    data = HabitatMixin.get_regions(period, subject)
    return jsonify(data)


summary.add_url_rule('/species/summary/',
                     view_func=SpeciesSummary.as_view('species-summary'))

summary.add_url_rule('/habitat/summary/',
                     view_func=HabitatSummary.as_view('habitat-summary'))
