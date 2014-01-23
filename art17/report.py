from flask import (
    Blueprint,
    views,
    render_template
)

from art17.mixins import SpeciesMixin


report = Blueprint('report', __name__)


class Report(views.View):

    methods = ['GET']

    def dispatch_request(self):
        context = self.get_context()
        return render_template(self.template_name, **context)


class SpeciesReport(SpeciesMixin, Report):

    template_name = 'report/species.html'

    def get_context(self):
        return {}


report.add_url_rule('/species/report/',
                    view_func=SpeciesReport.as_view('species-report'))
