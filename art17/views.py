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
    db,
    t_restricted_species,
)

from art17.common import get_default_period, admin_perm, expert_perm, \
    CONCLUSION_CLASSES, COUNTRY_ASSESSMENTS
from art17.forms import SummaryFilterForm


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
    return {'record_errors': record_errors}


@summary.app_context_processor
def inject_static():
    return {
        'CONCLUSION_CLASSES': CONCLUSION_CLASSES,
        'COUNTRY_ASSESSMENTS': COUNTRY_ASSESSMENTS,
    }


def record_errors(record):
    if isinstance(record, EtcDataSpeciesRegion):
        qs = EtcQaErrorsSpeciesManualChecked.query.filter_by(
            assesment_speciesname=record.assesment_speciesname,
            region=record.region,
            eu_country_code=record.eu_country_code,
        )
        return {e.field: {'text': e.text} for e in qs}
    raise ValueError("Invalid record type" + str(type(record)))


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
        self.setup_objects_and_data(period, subject, region)

        summary_filter_form = SummaryFilterForm(request.args)
        summary_filter_form.group.choices = get_groups(period)
        summary_filter_form.species.choices = get_species(period, group)
        summary_filter_form.region.choices = get_regions(period, species)

        current_selection = self.get_current_selection(group, species, region)
        annexes = self.get_annexes(species)
        context = {
            'objects': self.objects,
            'restricted_countries': self.restricted_countries,
            'regions': EtcDicBiogeoreg.query.all(),
            'summary_filter_form': summary_filter_form,
            'current_selection': current_selection,
            'annexes': annexes,
            'group': group,
        }

        return render_template('summary.html', **context)

    def get_current_selection(self, group, species, region):
        if not group and not species:
            return []
        current_selection = [group, species]
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


class SpeciesSummary(Summary, SpeciesMixin):

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


class Group(views.MethodView):

    def get(self):
        data = get_groups(request.args['period'])
        return jsonify(data)


class Species(views.MethodView):

    def get(self):
        period, group = request.args['period'], request.args['group']
        data = get_species(period, group)
        return jsonify(data)


class Regions(views.MethodView):

    def get(self):
        period, species = request.args['period'], request.args['species']
        data = get_regions(period, species)
        return jsonify(data)


summary.add_url_rule('/species/summary/',
                     view_func=SpeciesSummary.as_view('species-summary'))
summary.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

summary.add_url_rule('/species/summary/groups',
                     view_func=Group.as_view('species-summary-groups'))
summary.add_url_rule('/species/summary/species',
                     view_func=Species.as_view('species-summary-species'))
summary.add_url_rule('/species/summary/regions',
                     view_func=Regions.as_view('species-summary-regions'))
