from flask import (
    views,
    request,
    render_template,
    Blueprint,
    url_for,
    jsonify,
)
from art17.common import get_default_period
from art17.forms import ProgressFilterForm
from art17.models import Dataset, EtcDicBiogeoreg
from art17.summary import SpeciesMixin, HabitatMixin

progress = Blueprint('progress', __name__)


def user_is_expert(user):
    return True if user in ('maximiur', 'iurieetcbd') else False


def save_decision(output):
    if output['main_decision'] == 'A' and output['original_decision']:
        output['other_decisions'].append(output['original_decision'])
    else:
        output['other_decisions'].append(output['main_decision'])

    return output


def save_conclusion(output, decision, option, conclusion_type):
    if conclusion_type == 'overall assessment':
        output['method'] = option['range'] if option['method'] == 'MTX' else option['method']
    else:
        output['method'] = option['method']

    output['main_decision'] = decision
    output['original_decision'] = option['decision']
    output['overall'] = option['overall']
    output['user_id'] = option['user_id']
    output['conclusion'] = option['conclusion']

    return output


class Progress(views.View):

    methods = ['GET']

    def get_conclusions(self):
        conclusions = ['range', 'population', 'habitat',
                       'future prospects', 'overall assessment']
        return zip(conclusions, conclusions)

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

        current_selection = self.get_current_selection(
            period_name, group, conclusion)

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

    def get_current_selection(self, period_name, group, conclusion):
        if not group:
            return []
        current_selection = [period_name, group, conclusion]
        return current_selection


class SpeciesProgress(Progress, SpeciesMixin):
    template_name = 'progress/species.html'

    def process_cell(self, cell_options, conclusion_type):
        output = {
            'main_decision': '',
            'other_decisions': [],
            'method': '',
            'user_id': '',
        }

        for option in cell_options:
            decision = option['decision']
            user = option['user_id']
            # if current conclusion is acceptated
            if decision == 'OK':
                 if output['main_decision'] == 'END':
                     output['other_decisions'].append(decision)
                 else:
                     if output['main_decision'] != '':
                         output = save_decision(output)
                     output = save_conclusion(output, decision, option, conclusion_type)

            # else current conclusion is not acceptated
            else:
                if output['main_decision'] in ['OK', 'END']:
                    output['other_decisions'].append(decision)
                else:
                    if user_is_expert(user):
                        if output['main_decision'] != '':
                            if output['user_id'] != user and output['overall'] == 'MTX':
                                output['other_decisions'].append(decision)
                            else:
                                output = save_decision(output)
                                output = save_conclusion(output, 'A', option, conclusion_type)
                        else:
                            output = save_conclusion(output, 'A', option, conclusion_type)
                    elif decision:
                        if output['main_decision'] != '' and user_is_expert(output['user_id']):
                            output['other_decisions'].append(decision)
                        else:
                            output = save_conclusion(output, decision, option, conclusion_type)
        return output

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
                           self.model_manual_cls.user_id,
                           self.model_manual_cls.method_assessment,
                           self.model_manual_cls.method_range,
                           *fields)
            .filter_by(dataset_id=period)
        )

        data_dict = {}
        for entry in self.objects.all():
            fields = ('subject', 'region', 'decision', 'user_id',
                      'overall', 'range', 'method', 'conclusion')
            row = dict(zip(fields, entry))
            if not (row['subject'] and row['region']):
                continue

            if row['subject'] not in data_dict:
                data_dict[row['subject']] = {}
            if row['region'] and row['region'] not in data_dict[row['subject']]:
                data_dict[row['subject']][row['region']] = []
            data_dict[row['subject']][row['region']].append(row)

        ret_dict = {}
        for subject,region in data_dict.iteritems():
            ret_dict[subject] = {}
            for region, cell_options in region.iteritems():
                ret_dict[subject][region] = self.process_cell(cell_options, conclusion_type)

        return ret_dict

    def get_context(self):
        return {
            'groups_url': url_for('.species-progress-groups'),
        }


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'

    def setup_objects_and_data(self, period, group, conclusion_type):
        pass


@progress.route('/species/progress/groups', endpoint='species-progress-groups')
def _groups():
    data = SpeciesMixin.get_groups(request.args['period'])
    return jsonify(data)

progress.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

progress.add_url_rule('/habitat/progress/',
                     view_func=HabitatProgress.as_view('habitat-progress'))
