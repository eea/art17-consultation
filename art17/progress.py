from flask import views, request, render_template, Blueprint
from art17.common import get_default_period
from art17.forms import ProgressFilterForm
from art17.models import Dataset, EtcDicBiogeoreg
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
            'subjects': self.subjects_by_group(period, group),
            'regions': EtcDicBiogeoreg.query.all(),
            'species_data': self.setup_objects_and_data(period, group, conclusion),
        })

        return render_template(self.template_name, **context)


class SpeciesProgress(Progress, SpeciesMixin):
    template_name = 'progress/species.html'

    def get_conclusions(self):
        conclusions = ['range', 'population', 'habitat',
                       'future prospects', 'overall assessment']
        return zip(conclusions, conclusions)


    def setup_objects_and_data(self, period, group, conclusion_type):

        if conclusion_type == 'range':
            fields = (self.model_manual_cls.method_range,
                      self.model_manual_cls.conclusion_range)
        elif conclusion_type == 'population':
            fields = (self.model_manual_cls.method_population,
                      self.model_manual_cls.conclusion_population)
        elif conclusion_type == 'habitat':
            fields = (self.model_manual_cls.method_habitat,
                      self.model_manual_cls.conclusion_habitat)
        elif conclusion_type == 'future prospects':
            fields = (self.model_manual_cls.method_future,
                      self.model_manual_cls.conclusion_future)
        elif conclusion_type == 'overall assessment':
            fields = (self.model_manual_cls.method_assessment,
                      self.model_manual_cls.conclusion_assessment)
        else:
            return {}

        self.objects = (
            self.model_manual_cls.query
            .with_entities(self.model_manual_cls.assesment_speciesname,
                           self.model_manual_cls.region,
                           self.model_manual_cls.decision,
                           *fields)
            .filter_by(dataset_id=period)
        )

        data_dict = {}
        for entry in self.objects.all():
            # entry sample: ('Canis Lupus', 'ALP', decision, method, conclusion)
            if not (entry[0] and entry[1]):
                continue
            if entry[0] not in data_dict:
                data_dict[entry[0]] = {}
            if entry[1] and entry[1] not in data_dict[entry[0]]:
                data_dict[entry[0]][entry[1]] = []
            data_dict[entry[0]][entry[1]].append({
                'decision': entry[2],
                'method': entry[3],
                'conclusion': entry[4],
            })

        return data_dict


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'


progress.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

progress.add_url_rule('/habitat/progress/',
                     view_func=HabitatProgress.as_view('habitat-progress'))
