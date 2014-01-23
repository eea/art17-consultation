from flask import views, request, render_template, Blueprint
from art17.common import get_default_period
from art17.forms import ProgressFilterForm
from art17.models import Dataset
from art17.summary import SpeciesMixin, HabitatMixin

progress = Blueprint('progress', __name__)


class Progress(views.View):

    methods = ['GET']

    def get_context(self):
        return {}

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        conclusion = request.args.get('conclusion')

        progress_filter_form = ProgressFilterForm(request.args)
        progress_filter_form.group.choices = self.get_groups(period)
        progress_filter_form.conclusion.choices = self.get_conclusions()

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''

        current_selection = [period_name, group, conclusion]

        context = self.get_context()
        context.update({
            'progress_filter_form': progress_filter_form,
            'current_selection': current_selection,
            'period_name': period_name,
            'group': group,
            'conclusion': conclusion,
        })

        return render_template(self.template_name, **context)


class SpeciesProgress(Progress, SpeciesMixin):
    template_name = 'progress/species.html'

    def get_conclusions(self):
        conclusions = ['range', 'population', 'habitat',
                       'future prospects', 'overall assessment']
        return zip(conclusions, conclusions)


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'


progress.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

progress.add_url_rule('/habitat/progress/',
                     view_func=HabitatProgress.as_view('habitat-progress'))
