from flask import (
    views,
    request,
    render_template,
    Blueprint,
    url_for,
    g,
    abort,
    jsonify,
)
from sqlalchemy import and_
from werkzeug.datastructures import MultiDict
from art17.auth import current_user
from art17.common import (
    get_default_period,
    COUNTRY_ASSESSMENTS,
    MixinView,
    admin_perm,
)
from art17.forms import ProgressFilterForm
from art17.models import (
    Dataset, EtcDicBiogeoreg, EtcDicHdHabitat, db,
    EtcDicDecision, EtcDicMethod,
)
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.comments import SpeciesCommentCounter, HabitatCommentCounter

progress = Blueprint('progress', __name__)

DEFAULT_CONCLUSION = 'overall assessment'


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

    #return current_user.has_role('etc') or current_user.has_role('admin')
    return current_user.has_role('admin')


@progress.app_template_global('can_select_assessor')
def can_select_assessor():
    if not current_user.is_authenticated():
        return False

    return current_user.has_role('admin')


@progress.app_template_global('can_preview_progress')
def can_preview_progress():
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
        if option['method'] == 'MTX':
            output['method'] = option['range']
        else:
            output['method'] = option['method']
    else:
        output['method'] = option['method']

    output['main_decision'] = decision
    output['original_decision'] = option['decision']
    output['overall'] = option['overall']
    output['user_id'] = option['user_id']
    output['conclusion'] = option['conclusion']

    return output


def get_counts(comment_counts, subject, region):
    key = (subject, region)
    return {
        ct: comment_counts[ct].get(key, 0)
        for ct in ('user', 'all', 'wiki')
    }


class Progress(views.View):

    methods = ['GET']

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
                           self.model_cls.presence)
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

    def process_title(self, subject, region, conclusion_type, cell, presence,
                      comment_counts):
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
            details=COUNTRY_ASSESSMENTS.get(cell['conclusion'], '')
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
        if current_user.has_role('etc') or current_user.has_role('admin'):
            comms = get_counts(comment_counts, subject, region)
            title.append((
                "Unread comments for my conclusions: {user}\n" +
                "Unread comments for all conclusions: {all}\n" +
                "Unread comments for data sheet info: {wiki}").format(**comms)
            )
        return '\n'.join(title)

    def process_cell(self, subject, region, cell_options, conclusion_type,
                     presence_info, comment_counts):
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
                    output = save_conclusion(output, decision, option,
                                             conclusion_type)
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
        if output['main_decision']:
            presence = self.process_presence(presence_info)
            output['title'] = self.process_title(
                subject, region, conclusion_type, output, presence,
                comment_counts,
            )
            output['comment_counts'] = (
                "{user} {all} {wiki}"
                .format(**get_counts(comment_counts, subject, region))
            )

        return output

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        group = request.args.get('group')
        conclusion = request.args.get('conclusion') or DEFAULT_CONCLUSION
        assessor = request.args.get('assessor')
        extra = request.args.get('extra') or ''

        progress_filter_form = ProgressFilterForm(
            MultiDict(dict(period=period, group=group, conclusion=conclusion,
                           assessor=assessor, extra=extra))
        )
        progress_filter_form.group.choices = self.get_groups(period)
        progress_filter_form.conclusion.choices = self.get_conclusions()
        progress_filter_form.assessor.choices = (
            self.get_assessors(period, group)
        )

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''
        regions = (
            EtcDicBiogeoreg.query
            .with_entities(EtcDicBiogeoreg.reg_code)
            .filter_by(dataset_id=period)
            .order_by(EtcDicBiogeoreg.order)
        )

        current_selection = self.get_current_selection(
            period_name, group, conclusion)

        self.DECISION_DETAILS = self.get_decision_details()
        self.METHOD_DETAILS = self.get_method_details()

        presence = self.get_presence(period)
        data_dict = self.setup_objects_and_data(period, group, conclusion,
                                                assessor)
        comment_counts = self.get_comment_counts(period)
        ret_dict = {}
        for subject, region in data_dict.iteritems():
            ret_dict[subject] = {}
            for region, cell_options in region.iteritems():
                presence_info = presence.get(subject, {}).get(region, {})
                cell = self.process_cell(
                    subject, region, cell_options, conclusion, presence_info,
                    comment_counts,
                )
                ret_dict[subject][region] = cell

        context = self.get_context()
        context.update({
            'progress_filter_form': progress_filter_form,
            'current_selection': current_selection,
            'period_name': period_name,
            'group': group,
            'conclusion': conclusion,
            'subjects': self.subjects_by_group(period, group),
            'regions': regions.all(),
            'objects': ret_dict,
            'dataset': period_query,
            'summary_endpoint': self.summary_endpoint,
            'extra': extra,
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

    def get_comment_counts(self, period):
        return SpeciesCommentCounter(period, g.identity.id).get_counts()

    def setup_objects_and_data(self, period, group, conclusion_type, user_id):
        fields = self.get_progress_fields(conclusion_type)
        if not fields:
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
        if user_id:
            self.objects = self.objects.filter_by(user_id=user_id)

        if not admin_perm.can():
            self.objects = self.objects.filter_by(decision='OK')

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

        return data_dict

    def get_context(self):
        return {
            'groups_url': url_for('common.species-groups'),
            'assessors_url': url_for('progress.species-assessors'),
            'comparison_endpoint': 'progress.species-comparison',
        }


class HabitatProgress(Progress, HabitatMixin):
    template_name = 'progress/habitat.html'

    def get_conclusions(self):
        conclusions = ['range', 'area', 'future prospects',
                       'structure', 'overall assessment']
        return zip(conclusions, conclusions)

    def get_comment_counts(self, period):
        return HabitatCommentCounter(period, g.identity.id).get_counts()

    def setup_objects_and_data(self, period, group, conclusion_type, user_id):
        fields = self.get_progress_fields(conclusion_type)
        if not fields:
            return {}

        self.objects = (
            db.session.query(self.model_manual_cls)
            .join(EtcDicHdHabitat, and_(
                self.model_manual_cls.habitatcode == EtcDicHdHabitat.habcode,
                self.model_manual_cls.dataset_id == EtcDicHdHabitat.dataset_id
            ))
            .with_entities(self.model_manual_cls.subject,
                           self.model_manual_cls.region,
                           self.model_manual_cls.decision,
                           self.model_manual_cls.user_id,
                           self.model_manual_cls.method_assessment,
                           self.model_manual_cls.method_range,
                           *fields)
            .filter(self.model_manual_cls.dataset_id == period)
        )
        if user_id:
            self.objects = self.objects.filter(
                self.model_manual_cls.user_id == user_id)

        if not admin_perm.can():
            self.objects = self.objects.filter(
                self.model_manual_cls.decision == 'OK')

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

        return data_dict

    def get_context(self):
        return {
            'groups_url': url_for('common.habitat-groups'),
            'assessors_url': url_for('progress.habitat-assessors'),
            'comparison_endpoint': 'progress.habitat-comparison',
        }


class ComparisonView(MixinView, views.View):

    def dispatch_request(self):
        subject = request.args.get('subject')
        conclusion = request.args.get('conclusion')
        fields = self.mixin.get_progress_fields(conclusion)
        if not fields:
            abort(404)
        datasets = Dataset.query.order_by(Dataset.name).all()
        data = {}
        for d in datasets:
            regions = (
                self.mixin.model_manual_cls.query
                .with_entities(self.mixin.model_manual_cls.region,
                               *fields)
                .filter_by(
                    subject=subject, dataset=d,
                )
            )
            region_data = [
                dict(zip(('region', 'method', 'conclusion'), r))
                for r in regions
            ]
            data[d.name] = {r['region']: r for r in region_data}
        regions = (
            EtcDicBiogeoreg.query
            .with_entities(EtcDicBiogeoreg.reg_code)
            .distinct()
        )
        return render_template('progress/compare.html',
                               **{'data': data, 'regions': regions})


progress.add_url_rule('/species/progress/',
                      view_func=SpeciesProgress.as_view('species-progress'))
progress.add_url_rule('/habitat/progress/',
                      view_func=HabitatProgress.as_view('habitat-progress'))
progress.add_url_rule('/species/progress/compare/',
                      view_func=ComparisonView.as_view('species-comparison',
                                                       mixin=SpeciesMixin))
progress.add_url_rule('/habitat/progress/compare/',
                      view_func=ComparisonView.as_view('habitat-comparison',
                                                       mixin=HabitatMixin))

@progress.route('/species/progress/assessors', endpoint='species-assessors')
def species_assessors():
    data = SpeciesMixin.get_assessors(
        request.args.get('period'), request.args.get('group'))
    return jsonify(data)

@progress.route('/habitat/progress/assessors', endpoint='habitat-assessors')
def species_assessors():
    data = HabitatMixin.get_assessors(
        request.args.get('period'), request.args.get('group'))
    return jsonify(data)
