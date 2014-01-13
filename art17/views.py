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

from art17.common import get_default_period, admin_perm, expert_perm
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


def record_errors(record):
    if isinstance(record, EtcDataSpeciesRegion):
        qs = EtcQaErrorsSpeciesManualChecked.query.filter_by(
            assesment_speciesname=record.assesment_speciesname,
            region=record.region,
            eu_country_code=record.eu_country_code,
        )
        return {e.field: {'text': e.text} for e in qs}
    raise ValueError("Invalid record type" + str(type(record)))


def get_groups():
    group_field = EtcDataSpeciesRegion.group
    groups = (EtcDataSpeciesRegion.query.filter(group_field != None)
              .with_entities(group_field, group_field)
              .distinct()
              .order_by(group_field))
    return [('', '-')] + groups.all()


def get_species(group):
    blank_option = [('', '-')]
    if group is None:
        return blank_option
    group_field = EtcDataSpeciesRegion.group
    assesment_field = EtcDataSpeciesRegion.assesment_speciesname
    species = (EtcDataSpeciesRegion.query.filter(assesment_field != None)
               .filter(group_field == group)
               .with_entities(assesment_field, assesment_field)
               .distinct()
               .order_by(assesment_field))
    return blank_option + species.all()


def get_regions(species):
    blank_option = [('', 'All bioregions')]
    assesment_field = EtcDataSpeciesRegion.assesment_speciesname
    region_field = EtcDataSpeciesRegion.region
    regions = (EtcDataSpeciesRegion.query.filter(region_field != None)
               .filter(assesment_field == species)
               .with_entities(region_field, region_field)
               .distinct()
               .order_by(region_field))
    return blank_option + regions.all()


class Summary(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        subject = request.args.get('subject')
        group = request.args.get('group')
        species = request.args.get('species')
        region = request.args.get('region')
        self.setup_objects_and_data(period, subject, region)

        summary_filter_form = SummaryFilterForm(request.args)
        summary_filter_form.group.choices = get_groups()
        summary_filter_form.species.choices = get_species(group)
        summary_filter_form.region.choices = get_regions(species)

        current_selection = []
        if group and species:
            current_selection = [group, species]
            if region:
                region_name = EtcDicBiogeoreg.get_region_name(region)
                if region_name:
                    current_selection.append(region_name[0])

        context = {
            'objects': self.objects,
            'restricted_countries': self.restricted_countries,
            'regions': EtcDicBiogeoreg.query.all(),
            'summary_filter_form': summary_filter_form,
            'current_selection': current_selection,
        }
        return render_template('summary.html', **context)


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


class Species(views.MethodView):

    def get(self):
        data = get_species(request.args['group'])
        return jsonify(data)


class Regions(views.MethodView):

    def get(self):
        data = get_regions(request.args['species'])
        return jsonify(data)


summary.add_url_rule('/species/summary/',
                     view_func=SpeciesSummary.as_view('species-summary'))
summary.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

summary.add_url_rule('/species/summary/species',
                     view_func=Species.as_view('species-summary-species'))
summary.add_url_rule('/species/summary/regions',
                     view_func=Regions.as_view('species-summary-regions'))
