from flask import views, request, render_template, Blueprint
from art17.common import get_default_period
from art17.models import EtcDicBiogeoreg
from art17.summary import SpeciesMixin, HabitatMixin

progress = Blueprint('progress', __name__)


class Progress(views.View):

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        # conclusion = request.args.get('conclusion')
        context = {
            'subjects': self.subjects_by_group(period, group),
            'regions': EtcDicBiogeoreg.query.all(),
        }
        return render_template(self.template_name, **context)


class SpeciesProgress(Progress, SpeciesMixin):
    template_name = 'progress/species.html'


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'


progress.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

progress.add_url_rule('/habitat/progress/',
                     view_func=HabitatProgress.as_view('habitat-progress'))
