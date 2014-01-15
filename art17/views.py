from flask import (
    Blueprint,
    views,
    request,
    render_template,
    jsonify,
)

from art17.models import (
    EtcDicBiogeoreg,
    EtcDataSpeciesRegion,
    EtcQaErrorsSpeciesManualChecked,
    Dataset,
    db,
    t_restricted_species,
    EtcDataHabitattypeRegion)

from art17.common import (
    get_default_period,
    admin_perm,
    expert_perm,
    population_size_unit,
    population_ref,
    CONCLUSION_CLASSES,
    COUNTRY_ASSESSMENTS,
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
    }


@summary.app_template_filter('str2num')
def _str2num(value, default='N/A'):
    return str2num(value, default=default)


def record_errors(record):
    if isinstance(record, EtcDataSpeciesRegion):
        qs = EtcQaErrorsSpeciesManualChecked.query.filter_by(
            assesment_speciesname=record.assesment_speciesname,
            region=record.region,
            eu_country_code=record.eu_country_code,
        )
        return {
            e.field: {'text': e.text, 'suspect_value': e.suspect_value}
            for e in qs
        }
    raise ValueError("Invalid record type" + str(type(record)))


def format_error(error, record, field):
    if field in ('range_surface_area', 'population_yearly_magnitude',
                 'complementary_favourable_range',
                 'complementary_favourable_range_q',
                 'range_yearly_magnitude',
                 'conclusion_range',
                 'percentage_range_surface_area',
                 'complementary_favourable_population_q',
                 'complementary_favourable_population',
                 'filled_complementary_favourable_population'):
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


def get_groups(period):
    group_field = EtcDataSpeciesRegion.group
    dataset_id_field = EtcDataSpeciesRegion.dataset_id
    groups = (
        EtcDataSpeciesRegion.query
        .filter(group_field != None, dataset_id_field == period)
        .with_entities(group_field, group_field)
        .distinct()
       .order_by(group_field)
       .all()
    )
    return [('', '-')] + groups


def get_species(period, group):
    blank_option = [('', '-')]
    if group is None:
        return blank_option
    group_field = EtcDataSpeciesRegion.group
    dataset_id_field = EtcDataSpeciesRegion.dataset_id
    assesment_field = EtcDataSpeciesRegion.assesment_speciesname
    species = (
        EtcDataSpeciesRegion.query
        .filter(assesment_field != None)
        .filter(group_field == group)
        .filter(dataset_id_field == period)
        .with_entities(assesment_field, assesment_field)
        .distinct()
        .order_by(assesment_field)
        .all()
    )
    return blank_option + species


def get_regions(period, species):
    blank_option = [('', 'All bioregions')]

    assesment_field = EtcDataSpeciesRegion.assesment_speciesname
    reg_field = EtcDataSpeciesRegion.region
    reg_code_field = EtcDicBiogeoreg.reg_code
    reg_name_field = EtcDicBiogeoreg.reg_name
    dataset_id_field = EtcDataSpeciesRegion.dataset_id

    regions = (
        EtcDicBiogeoreg.query
        .join(EtcDataSpeciesRegion, reg_code_field == reg_field)
        .filter(assesment_field == species)
        .filter(dataset_id_field == period)
        .with_entities(reg_field, reg_name_field)
        .distinct()
        .order_by(reg_field)
        .all()
    )
    return blank_option + regions


class Summary(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        subject = request.args.get(self.subject_name)
        group = request.args.get('group')
        species = request.args.get('species')
        region = request.args.get('region')
        self.objects = []
        self.restricted_countries = []
        self.setup_objects_and_data(period, subject, region)

        summary_filter_form = SummaryFilterForm(request.args)
        summary_filter_form.group.choices = get_groups(period)
        summary_filter_form.species.choices = get_species(period, group)
        summary_filter_form.region.choices = get_regions(period, species)

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''

        current_selection = self.get_current_selection(
            period_name, group, species, region)
        annexes = self.get_annexes(species)
        context = {
            'objects': self.objects,
            'restricted_countries': self.restricted_countries,
            'regions': EtcDicBiogeoreg.query.all(),
            'summary_filter_form': summary_filter_form,
            'current_selection': current_selection,
            'annexes': annexes,
            'group': group,
            'period_name': period_name,
        }

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


class Progress(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        # conclusion = request.args.get('conclusion')
        context = {
            'subjects': self.subjects_by_group(period, group),
            'regions': EtcDicBiogeoreg.query.all(),
        }
        return render_template('progress.html', **context)


class SpeciesMixin(object):

    model_cls = EtcDataSpeciesRegion
    subject_name = 'species'

    def objects_by_group(self, period, group):
        return self.model_cls.query.filter_by(group=group, dataset_id=period)

    def subjects_by_group(self, period, group):
        qs = db.session.query(self.model_cls.speciesname).\
            filter_by(group=group, dataset_id=period).distinct()
        return [row[0] for row in qs]


class HabitatMixin(object):

    model_cls = EtcDataHabitattypeRegion
    subject_name = 'habitat'


class SpeciesSummary(Summary, SpeciesMixin):

    template_name = 'species_summary.html'

    def setup_objects_and_data(self, period, subject, region):
        self.objects = []
        self.restricted_countries = []
        filter_args = {}
        if subject:
            filter_args['assesment_speciesname'] = subject
        else:
            return False
        self.restricted_countries = [r[0] for r in db.session.query(
            t_restricted_species.c.eu_country_code).
            filter(t_restricted_species.c.assesment_speciesname == subject.lower()).
            filter(t_restricted_species.c.show_data == 0).all()]
        if region:
            filter_args['region'] = region
        if filter_args:
            filter_args['dataset_id'] = period
            self.objects = self.model_cls.query.filter_by(**filter_args)
        return True


class SpeciesProgress(Progress, SpeciesMixin):
    pass


class HabitatSummary(Summary, HabitatMixin):

    template_name = 'habitat_summary.html'

    def setup_objects_and_data(self, period, subject, region):
        pass


@summary.route('/species/summary/groups', endpoint='species-summary-groups')
def _groups():
    data = get_groups(request.args['period'])
    return jsonify(data)


@summary.route('/species/summary/species', endpoint='species-summary-species')
def _species():
    period, group = request.args['period'], request.args['group']
    data = get_species(period, group)
    return jsonify(data)


@summary.route('/species/summary/regions', endpoint='species-summary-regions')
def _regions():
    period, species = request.args['period'], request.args['species']
    data = get_regions(period, species)
    return jsonify(data)


summary.add_url_rule('/species/summary/',
                     view_func=SpeciesSummary.as_view('species-summary'))
summary.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

summary.add_url_rule('/habitat/summary/',
                     view_func=HabitatSummary.as_view('habitat-summary'))
