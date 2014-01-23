from flask import (
    Blueprint,
    views,
    request,
    render_template
)

from art17.common import get_default_period
from art17.mixins import SpeciesMixin


report = Blueprint('report', __name__)


class Report(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        self.objects = []
        self.setup_objects_and_data(period, group)
        context = self.get_context()
        context.update({
            'objects': self.objects,
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
        return {}


report.add_url_rule('/species/report/',
                    view_func=SpeciesReport.as_view('species-report'))
