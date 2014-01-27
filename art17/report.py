from flask import (
    Blueprint,
    views,
    request,
    url_for,
    render_template,
    jsonify,
)

from art17.common import get_default_period
from art17.mixins import SpeciesMixin
from art17.forms import ReportFilterForm


report = Blueprint('report', __name__)


class Report(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        country = request.args.get('country')
        self.objects = []
        self.setup_objects_and_data(period, group)

        report_filter_form = ReportFilterForm(request.args)
        report_filter_form.group.choices = self.get_groups(period)
        report_filter_form.country.choices = self.get_countries(period)
        report_filter_form.region.choices = self.get_regions(period, country)

        context = self.get_context()
        context.update({
            'objects': self.objects,
            'report_filter_form': report_filter_form,

        })
        return render_template(self.template_name, **context)


class SpeciesReport(SpeciesMixin, Report):

    template_name = 'report/species.html'

    def setup_objects_and_data(self, period, group):
        filter_args = {}
        if group:
            filter_args['group'] = group
        else:
            return
        filter_args['dataset_id'] = period
        self.objects = self.model_cls.query.filter_by(**filter_args)

    def get_context(self):
        return {
            'regions_url': url_for('.species-report-regions'),
        }


@report.route('/species/report/regions', endpoint='species-report-regions')
def _regions():
    period, country = request.args['period'], request.args['country']
    data = SpeciesMixin.get_regions_by_country(period, country)
    return jsonify(data)


report.add_url_rule('/species/report/',
                    view_func=SpeciesReport.as_view('species-report'))
