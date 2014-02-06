from flask import (
    views,
    request,
    render_template,
    Blueprint,
    url_for,
    jsonify,
)
from art17.auth import current_user
from art17.common import get_default_period, COUNTRY_ASSESSMENTS
from art17.forms import ProgressFilterForm
from art17.models import (
    Dataset, EtcDicBiogeoreg, EtcDicHdHabitat, db,
    EtcDicDecision, EtcDicMethod,
)
from art17.summary import SpeciesMixin, HabitatMixin

progress = Blueprint('progress', __name__)


@progress.app_template_filter('methodify')
def methodify(s):
    """
    Append 'M' to '0' and '00' from old application
    """
    return 'M' + s if s in ('0', '00') else s


@progress.app_template_global('can_view_details')
def can_view_details():
    if not current_user.is_authenticated():
        return False

    return current_user.has_role('etc') or current_user.has_role('admin')


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
        return {}

    def get_context(self):
        return {}

    def get_decision_details(self):
        d = dict((r.decision, r.details) for r in EtcDicDecision.query.all())
        d['no decision'] = 'Auto'
        return d

    def get_method_details(self):
        return dict((r.method, r.details) for r in EtcDicMethod.query.all())

    def get_presence(self, period):
        presence_qs = (
            self.model_cls.query
            .with_entities(self.model_cls.subject,
                           self.model_cls.region,
                           self.model_cls.eu_country_code,
                           self.model_cls.habitattype_type_asses)
            .filter_by(dataset_id=period)
        )
        presence = {}
        for report in presence_qs:
            fields = ('subject', 'region', 'eu_country_code',
                      'species_type_asses')
            row = dict(zip(fields, report))
            if row['subject'] not in presence:
                presence[row['subject']] = {}
            if row['region']:
                if row['region'] not in presence[row['subject']]:
                    presence[row['subject']][row['region']] = []
                presence[row['subject']][row['region']].append(row)
        return presence

    def process_presence(self, presence):
        occasional = (
            ','.join([row['eu_country_code']
                      for row in presence if row['species_type_asses'] == 0])
        )
        present = (
            ','.join([row['eu_country_code']
                      for row in presence if row['species_type_asses'] != 0])
        )
        return dict(occasional=occasional, present=present)

    def process_title(self, subject, region, conclusion_type, cell, presence):
        title = []
        title.append(
            'Species: {species}, Region: {region}'.format(
                species=subject, region=region))
        if presence['present']:
            title.append('Reported as present by: ' + presence['present'])
        if presence['occasional']:
            title.append('Reported as occasional by: ' + presence['occasional'])
        title.append('Assessment {type} : {details}'.format(
            type=conclusion_type,
            details=COUNTRY_ASSESSMENTS.get(cell['conclusion'],'')
        ))
        if current_user.has_role('etc') or current_user.has_role('admin'):
            title.append('Decision: {main} ({details})'.format(
                main=cell['main_decision'],
                details=self.DECISION_DETAILS.get(cell['main_decision'], 'Auto')
            ))
        title.append('Method {method} ({details})'.format(
                method=cell['method'],
                details=self.METHOD_DETAILS.get(cell['method'], '')
        ))
        return '\n'.join(title)

    def process_cell(self, cell_options, conclusion_type):
        output = {
            'main_decision': '',
            'other_decisions': [],
            'method': '',
            'user_id': '',
        }

        for option in cell_options:
            decision = option['decision'] or ''
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

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        conclusion = request.args.get('conclusion')

        progress_filter_form = ProgressFilterForm(request.args)
        progress_filter_form.group.choices = self.get_groups(period)
        progress_filter_form.conclusion.choices = self.get_conclusions()

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''
        regions = (
            EtcDicBiogeoreg.query
            .with_entities(EtcDicBiogeoreg.reg_code)
            .filter_by(dataset_id=period)
        )

        current_selection = self.get_current_selection(
            period_name, group, conclusion)

        self.DECISION_DETAILS = self.get_decision_details()
        self.METHOD_DETAILS = self.get_method_details()
        context = self.get_context()
        context.update({
            'progress_filter_form': progress_filter_form,
            'current_selection': current_selection,
            'period_name': period_name,
            'group': group,
            'conclusion': conclusion,
            'subjects': self.subjects_by_group(period, group),
            'regions': regions.all(),
            'objects': self.setup_objects_and_data(period, group, conclusion),
        })

        return render_template(self.template_name, **context)

    def get_current_selection(self, period_name, group, conclusion):
        if not group:
            return []
        current_selection = [period_name, group, conclusion]
        return current_selection


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
            .with_entities(self.model_manual_cls.subject,
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
            if row['region']:
                if row['region'] not in data_dict[row['subject']]:
                    data_dict[row['subject']][row['region']] = []
                data_dict[row['subject']][row['region']].append(row)

        presence = self.get_presence(period)
        ret_dict = {}
        for subject, region in data_dict.iteritems():
            ret_dict[subject] = {}
            for region, cell_options in region.iteritems():
                cell = self.process_cell(cell_options, conclusion_type)
                ret_dict[subject][region] = cell
                if cell['main_decision']:
                    pi = presence.get(subject, {}).get(region, {})
                    presence_info = self.process_presence(pi)
                    ret_dict[subject][region]['title'] = self.process_title(
                        subject, region, conclusion_type, cell, presence_info
                    )

        return ret_dict

    def get_context(self):
        return {
            'groups_url': url_for('.species-progress-groups'),
            'summary_endpoint': 'summary.species-summary',
        }


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'

    def get_conclusions(self):
        conclusions = ['range', 'area', 'future prospects',
                       'structure', 'overall assessment']
        return zip(conclusions, conclusions)

    def setup_objects_and_data(self, period, group, conclusion_type):
        if conclusion_type == 'range':
            fields = (self.model_manual_cls.method_range,
                      self.model_manual_cls.conclusion_range)
        elif conclusion_type == 'area':
            fields = (self.model_manual_cls.method_area,
                      self.model_manual_cls.conclusion_area)
        elif conclusion_type == 'future prospects':
            fields = (self.model_manual_cls.method_future,
                      self.model_manual_cls.conclusion_future)
        elif conclusion_type == 'structure':
            fields = (self.model_manual_cls.method_structure,
                      self.model_manual_cls.conclusion_structure)
        elif conclusion_type == 'overall assessment':
            fields = (self.model_manual_cls.method_assessment,
                      self.model_manual_cls.conclusion_assessment)
        else:
            return {}

        self.objects = (
            db.session.query(self.model_manual_cls)
            .join(EtcDicHdHabitat, self.model_manual_cls.habitatcode ==
                  EtcDicHdHabitat.habcode)
            .with_entities(self.model_manual_cls.subject,
                           EtcDicHdHabitat.shortname,
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
            processed_entry = tuple([' - '.join(entry[0:2])] + list(entry[2:]))
            row = dict(zip(fields, processed_entry))
            if not (row['subject'] and row['region']):
                continue

            if row['subject'] not in data_dict:
                data_dict[row['subject']] = {}
            if row['region'] and row['region'] not in data_dict[row['subject']]:
                data_dict[row['subject']][row['region']] = []
            data_dict[row['subject']][row['region']].append(row)

        presence = self.get_presence(period)
        ret_dict = {}
        for subject,region in data_dict.iteritems():
            ret_dict[subject] = {}
            for region, cell_options in region.iteritems():
                cell = self.process_cell(cell_options, conclusion_type)
                ret_dict[subject][region] = cell
                if cell['main_decision']:
                    pi = presence.get(subject, {}).get(region, {})
                    presence_info = self.process_presence(pi)
                    ret_dict[subject][region]['title'] = self.process_title(
                        subject, region, conclusion_type, cell, presence_info
                    )

        return ret_dict

    def get_context(self):
        return {
            'groups_url': url_for('.habitat-progress-groups'),
            'summary_endpoint': 'summary.habitat-summary',
        }


@progress.route('/species/progress/groups', endpoint='species-progress-groups')
def _groups():
    data = SpeciesMixin.get_groups(request.args['period'])
    return jsonify(data)


@progress.route('/habitat/progress/groups', endpoint='habitat-progress-groups')
def _habitat_groups():
    data = HabitatMixin.get_groups(request.args['period'])
    return jsonify(data)


progress.add_url_rule('/species/progress/',
                     view_func=SpeciesProgress.as_view('species-progress'))

progress.add_url_rule('/habitat/progress/',
                     view_func=HabitatProgress.as_view('habitat-progress'))
