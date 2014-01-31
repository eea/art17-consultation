from flask import (
    Blueprint,
    views,
    request,
    url_for,
    render_template,
    jsonify,
)

from art17.common import get_default_period
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.forms import ReportFilterForm
from art17.models import Dataset, EtcDicBiogeoreg, DicCountryCode

report = Blueprint('report', __name__)


class Report(views.View):

    def get_context(self):
        return {}

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        country = request.args.get('country')
        region = request.args.get('region')

        self.objects = []
        self.setup_objects_and_data(period, group, country)

        countries = self.get_countries(period)
        regions = self.get_regions_by_country(period, country)
        report_filter_form = ReportFilterForm(request.args)
        report_filter_form.group.choices = self.get_groups(period)
        report_filter_form.country.choices = countries
        report_filter_form.region.choices = regions

        countries_map = dict(countries)
        regions_map = dict(regions)
        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''

        current_selection = self.get_current_selection(
            period_name, group,
            countries_map.get(country, country),
            regions_map.get(region, region)
        )

        context = self.get_context()
        context.update({
            'objects': self.objects,
            'current_selection': current_selection,
            'report_filter_form': report_filter_form,
            'region': region,
            'country': country,
            'show_species_report_headers': True,
        })

        return render_template(self.template_name, **context)

    def get_current_selection(self, period_name, group,
                              country_name, region_name):
        if not group:
            return []
        return [period_name, group, country_name, region_name]


class SpeciesReport(SpeciesMixin, Report):

    template_name = 'report/species.html'

    def setup_objects_and_data(self, period, group, country):
        filter_args = {}
        if group:
            filter_args['group'] = group
        else:
            return
        if country:
            filter_args['eu_country_code'] = country

        filter_args['dataset_id'] = period
        self.objects = (
            self.model_cls.query
            .filter_by(**filter_args)
            .order_by(self.model_cls.speciesname)
        )

    def get_context(self):
        return {
            'regions_url': url_for('.species-report-regions'),
            'groups_url': url_for('.species-report-groups'),
        }


class HabitatReport(HabitatMixin, Report):

    template_name = 'report/habitat.html'

    def setup_objects_and_data(self, period, group, country):
        return []


@report.route('/species/report/groups', endpoint='species-report-groups')
def _groups():
    data = SpeciesMixin.get_groups(request.args['period'])
    return jsonify(data)


@report.route('/species/report/regions', endpoint='species-report-regions')
def _regions():
    period, country = request.args['period'], request.args['country']
    data = SpeciesMixin.get_regions_by_country(period, country)
    return jsonify(data)


report.add_url_rule('/species/report/',
                    view_func=SpeciesReport.as_view('species-report'))

report.add_url_rule('/habitat/report/',
                    view_func=HabitatReport.as_view('habitat-report'))
