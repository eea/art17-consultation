from datetime import datetime, date
from flask import (
    Blueprint,
    views,
    request,
    render_template,
    jsonify,
    url_for,
    flash,
    abort,
    g,
)
from flask.ext.principal import PermissionDenied
from sqlalchemy.exc import IntegrityError
from werkzeug.datastructures import MultiDict
from werkzeug.utils import redirect
from art17.auth import current_user

from art17.models import (
    EtcDicBiogeoreg,
    EtcDataSpeciesRegion,
    EtcQaErrorsSpeciesManualChecked,
    Dataset,
    db,
    t_restricted_species,
    EtcDataHabitattypeRegion,
    EtcQaErrorsHabitattypeManualChecked,
    EtcDicMethod,
    EtcDicDecision,
    RegisteredUser,
)

from art17.mixins import SpeciesMixin, HabitatMixin

from art17.common import (
    get_default_period,
    admin_perm,
    expert_perm,
    sta_perm,
    etc_perm,
    population_size_unit,
    population_ref,
    get_range_conclusion_value,
    get_population_conclusion_value,
    get_future_conclusion_value_for_species,
    get_future_conclusion_value_for_habitat,
    get_assesm_conclusion_value_for_species,
    get_assesm_conclusion_value_for_habitat,
    get_habitat_conclusion_value,
    get_coverage_conclusion_value,
    get_struct_conclusion_value,
    get_original_record_url,
    get_title_for_species_country,
    get_title_for_habitat_country,
    CONCLUSION_CLASSES,
    COUNTRY_ASSESSMENTS,
    QUALITIES,
    population_size_unit_title,
    CONTRIB_METHOD,
    CONTRIB_CONCLUSION,
    get_config,
    TREND_OPTIONS, TREND_OPTIONS_OVERALL, NATURE_OF_CHANGE_OPTIONS,
    HABITAT_OPTIONS, get_default_ms)
from art17.forms import (
    SummaryFilterForm,
    SummaryManualFormSpecies,
    SummaryManualFormHabitat,
    SummaryManualFormHabitatRef,
    SummaryManualFormSpeciesRef,
    all_fields,
    SummaryManualFormSpeciesSTA,
    SummaryManualFormSpeciesRefSTA,
    SummaryManualFormHabitatRefSTA,
    SummaryManualFormHabitatSTA,
)
from art17.utils import str2num, parse_semicolon, str1num


summary = Blueprint('summary', __name__)

DATE_FORMAT = '%d/%m/%Y %H:%M'
DATE_FORMAT_PH = '%Y-%m-%d %H:%M:%S'


@summary.route('/')
def homepage():
    config = get_config()
    user_credentials = g.get('user_credentials', {})
    user_id = user_credentials.get('user_id')
    user_authenticated = RegisteredUser.query.get(user_id) if user_id else None

    return render_template('homepage.html', **{
        'start_date': config.start_date,
        'end_date': config.end_date,
        'today': date.today(),
        'user_authenticated': user_authenticated,
    })


@summary.app_template_global('can_view')
def can_view(record, countries):
    return (admin_perm.can() or expert_perm.can() or
            record.eu_country_code not in countries)


@summary.app_template_global('can_edit')
def can_edit(record):
    if current_user.is_anonymous():
        return False

    if record.deleted:
        return False

    if record.dataset.is_readonly:
        return False

    if record.user_id == current_user.id:
        return True

    return etc_perm.can() or admin_perm.can()


@summary.app_template_global('can_delete')
def can_delete(record):
    if current_user.is_anonymous():
        return False

    if record.dataset.is_readonly:
        return False

    return record.user_id == current_user.id


@summary.app_template_global('can_view_decision')
def can_view_decision(record):
    # TODO: check acl_manager code for checkPermissionViewDecision
    return expert_perm.can() or admin_perm.can()


@summary.app_template_global('can_update_decision')
def can_update_decision(record):
    return expert_perm.can() or admin_perm.can()


@summary.app_template_global('can_add_conclusion')
def can_add_conclusion(dataset, zone, subject, region=None):
    """
    Zone: one of 'species', 'habitat'
    """
    zone_cls_mapping = {'species': SpeciesSummary, 'habitat': HabitatSummary}
    if not dataset:
        return False
    record_exists = False
    if region and not current_user.is_anonymous():
        record_exists = zone_cls_mapping[zone].get_manual_record(
            dataset.id, subject, region, current_user.id)
    return not dataset.is_readonly and (sta_perm.can() or admin_perm.can()) \
        and not record_exists


@summary.app_template_global('can_select_MS')
def can_select_MS():
    return sta_perm.can()


@summary.app_context_processor
def inject_fuctions():
    return {
        'record_errors': record_errors,
        'parse_qa_errors': parse_qa_errors,
        'population_size_unit': population_size_unit,
        'population_size_unit_title': population_size_unit_title,
        'population_ref': population_ref,
        'get_range_conclusion_value': get_range_conclusion_value,
        'get_population_conclusion_value': get_population_conclusion_value,
        'get_future_conclusion_value_for_species': get_future_conclusion_value_for_species,
        'get_future_conclusion_value_for_habitat': get_future_conclusion_value_for_habitat,
        'get_assesm_conclusion_value_for_species': get_assesm_conclusion_value_for_species,
        'get_assesm_conclusion_value_for_habitat': get_assesm_conclusion_value_for_habitat,
        'get_habitat_conclusion_value': get_habitat_conclusion_value,
        'get_coverage_conclusion_value': get_coverage_conclusion_value,
        'get_struct_conclusion_value': get_struct_conclusion_value,
        'get_original_record_url': get_original_record_url,
        'get_title_for_species_country': get_title_for_species_country,
        'get_title_for_habitat_country': get_title_for_habitat_country,
    }


@summary.app_context_processor
def inject_static():
    make_tooltip = lambda d: '\n' + '\n'.join(['%s: %s' % (k, v) for k, v in d])
    return {
        'expert_perm': expert_perm,
        'CONCLUSION_CLASSES': CONCLUSION_CLASSES,
        'COUNTRY_ASSESSMENTS': COUNTRY_ASSESSMENTS,
        'CONTRIB_METHOD': CONTRIB_METHOD,
        'CONTRIB_CONCLUSION': CONTRIB_CONCLUSION,
        'QUALITIES': QUALITIES,
        'ASSESSMENT_DETAILS': dict(
            db.session.query(EtcDicMethod.method, EtcDicMethod.details)
        ),
        'DECISION_DETAILS': dict(
            db.session.query(EtcDicDecision.decision, EtcDicDecision.details)
        ),
        'TREND_TOOLTIP': make_tooltip(TREND_OPTIONS),
        'TREND_ALL_TOOLTIP': make_tooltip(TREND_OPTIONS_OVERALL),
        'NATURE_TOOLTIP': make_tooltip(NATURE_OF_CHANGE_OPTIONS),
        'HABITAT_TOOLTIP': make_tooltip(HABITAT_OPTIONS),
    }


@summary.app_template_filter('str2num')
def _str2num(value, default='N/A'):
    return str2num(value, default=default)


@summary.app_template_filter('str1num')
def _str1num(value, default='N/A'):
    return str1num(value, default=default)


@summary.app_template_filter('parse_semicolon')
def _parse_semicolon(value, sep='<br/>'):
    return parse_semicolon(value, sep=sep)


@summary.app_template_filter('get_quality')
def get_quality(value, default='N/A'):
    if value and value[0].upper() in QUALITIES:
        return value[0]
    return default


@summary.app_template_filter('format_date')
def format_date(value):
    if not value:
        return ''
    try:
        date = datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return value
    return date.strftime('%m/%y')


def record_errors(record):
    if isinstance(record, (EtcDataSpeciesRegion, EtcDataHabitattypeRegion)):
        error_cls = EtcQaErrorsSpeciesManualChecked
    elif isinstance(record, EtcDataHabitattypeRegion):
        error_cls = EtcQaErrorsHabitattypeManualChecked
    else:
        raise ValueError("Invalid record type" + str(type(record)))
    qs = error_cls.query.filter_by(
        subject=record.subject,
        region=record.region,
        eu_country_code=record.eu_country_code,
        dataset_id=record.dataset_id,
    )
    return {
        e.field: {'text': e.text, 'suspect_value': e.suspect_value}
        for e in qs
    }


def format_error(error, record, field):
    if error.get('suspect_value', ''):
        return '%s: %s' % (error['text'], error['suspect_value'])
    return error['text']


def parse_qa_errors(fields, record, qa_errors):
    title = []
    classes = []
    if isinstance(fields, str):
        fields = [fields]
    for field in fields:
        if field in qa_errors:
            title.append(format_error(qa_errors[field], record, field))
            classes.append('qa_error')
    return '<br/>'.join(title), ' '.join(classes)


class Summary(views.View):

    methods = ['GET', 'POST']

    def get_best_automatic(self):
        period = request.args.get('period') or get_default_period()
        subject = request.args.get('subject')
        region = request.args.get('region')
        best = (
            self.model_auto_cls.query
            .filter_by(dataset_id=period, subject=subject, region=region)
            .join(
                EtcDicMethod,
                self.model_auto_cls.assessment_method == EtcDicMethod.method
            )
        ).all()
        cmpf = (
            lambda x, y:
            -1 if x.assessment_method == '00' else cmp(x.order, y.order)
        )
        best.sort(cmp=cmpf)
        values = {}
        for f in all_fields(self.manual_form_cls()):
            attr = f.name
            for ass in best:
                if getattr(ass, attr, ''):
                    values[attr] = getattr(ass, attr)
                    break
        return values

    def can_touch(self, assessment):
        if current_user.is_anonymous():
            return False
        if not assessment:
            return admin_perm.can() or sta_perm.can()
        else:
            return admin_perm.can() or etc_perm.can() or (
                sta_perm.can() and assessment.user == current_user)

    def must_edit_ref(self, assessment):
        if not current_user.is_authenticated() or not assessment:
            return False
        if assessment.user_id == current_user.id:
            return False

        return etc_perm.can() or admin_perm.can()

    def get_form_cls(self):
        if not can_select_MS():
            return self.manual_form_cls, self.manual_form_ref_cls
        return self.manual_form_sta_cls, self.manual_form_ref_sta_cls

    def get_manual_form(self, data=None, period=None, action=None):
        manual_form_cls, manual_form_ref_cls = self.get_form_cls()
        if action == 'edit':
            filters = {
                'region': request.args.get('edit_region'),
                'user_id': request.args.get('edit_user'),
                'subject': request.args.get('subject')
            }
            manual_assessment = self.model_manual_cls.query.filter_by(
                **filters
            ).first_or_404()
        else:
            manual_assessment = None
            data = data or MultiDict(self.get_default_values())

        if not self.must_edit_ref(manual_assessment):
            form = manual_form_cls(formdata=data, obj=manual_assessment)
        else:
            form = manual_form_ref_cls(formdata=data, obj=manual_assessment)
        form.setup_choices(dataset_id=period)
        return form, manual_assessment

    def dispatch_request(self):
        period = request.args.get('period') or get_default_period()
        subject = request.args.get('subject')
        group = request.args.get('group')
        region = request.args.get('region')
        action = request.args.get('action')
        rowid = request.args.get('rowid')

        self.objects = []
        self.restricted_countries = []
        self.auto_objects = []
        self.manual_objects = []
        self.setup_objects_and_data(period, subject, region)
        group = group or self.get_group_for_subject(subject)

        regions = self.get_regions(period, subject)
        summary_filter_form = SummaryFilterForm(
            MultiDict(dict(period=period, group=group, subject=subject,
                           region=region)
                      )
        )
        summary_filter_form.group.choices = self.get_groups(period)
        summary_filter_form.subject.choices = self.get_subjects(period, group)
        summary_filter_form.region.choices = regions

        manual_form, manual_assessment = self.get_manual_form(
            request.form, period=period, action=action,
        )
        manual_form.region.choices = self.get_regions(period, subject, True)[1:]
        if not request.form.get('region'):
            manual_form.region.process_data(region)
        if hasattr(manual_form, 'MS'):
            manual_form.kwargs = dict(subject=subject, period=period)
            manual_form.MS.choices = self.get_MS(subject, region, period)

        if request.method == 'POST':
            if manual_form.validate(subject=subject, period=period):
                if not self.can_touch(manual_assessment):
                    raise PermissionDenied()

                if not manual_assessment:
                    manual_assessment = self.model_manual_cls(subject=subject)
                    manual_form.populate_obj(manual_assessment)
                    manual_assessment.last_update = datetime.now().strftime(DATE_FORMAT)
                    manual_assessment.user_id = current_user.id
                    manual_assessment.dataset_id = period
                    db.session.flush()
                    db.session.add(manual_assessment)
                    try:
                        db.session.commit()
                    except IntegrityError:
                        db.session.rollback()
                        flash('A record with the same keys exist. Cannot add',
                              'error')
                    else:
                        flash('Conclusion added successfully')
                    manual_assessment = None
                else:
                    manual_form.populate_obj(manual_assessment)
                    manual_assessment.last_update = datetime.now().strftime(DATE_FORMAT)
                    db.session.add(manual_assessment)
                    db.session.commit()
                    flash('Conclusion edited successfully')
                    home_url = url_for(self.summary_endpoint, period=period,
                                       subject=subject, region=region)
                    if rowid:
                        home_url += '#man-row-' + rowid
                    return redirect(home_url)
            else:
                flash('Please correct the errors below and try again.')

        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ''

        current_selection = self.get_current_selection(
            period_name, group, subject, region)
        annexes = self.get_annexes(subject)
        context = self.get_context()
        context.update({
            'objects': self.objects,
            'auto_objects': self.auto_objects,
            'manual_objects': self.view_conclusions(self.manual_objects),
            'restricted_countries': self.restricted_countries,
            'regions': regions,
            'summary_filter_form': summary_filter_form,
            'manual_form': manual_form,
            'manual_assessment': manual_assessment,
            'edit_ref': self.must_edit_ref(manual_assessment),
            'current_selection': current_selection,
            'annexes': annexes,
            'group': group,
            'subject': subject,
            'region': region,
            'period_name': period_name,
            'dataset': period_query,
        })

        return render_template(self.template_name, **context)

    def get_current_selection(self, period_name, group, subject, region):
        if not subject:
            return []
        current_selection = [period_name, group, subject]
        if region:
            region_name = EtcDicBiogeoreg.get_region_name(region)
            if region_name:
                current_selection.append(region_name[0])
        else:
            current_selection.append('All bioregions')
        return current_selection

    def get_annexes(self, species):
        annexes_results = (
            EtcDataSpeciesRegion.query
            .with_entities('annex_II', 'annex_IV', 'annex_V', 'priority')
            .filter(EtcDataSpeciesRegion.subject == species)
            .distinct()
            .first()
        )
        if not annexes_results:
            return []
        annexes = list(annexes_results)
        try:
            priority = int(annexes.pop())
        except (ValueError, TypeError):
            priority = 0
        if annexes[0] and priority:
            annexes[0] += '*'
        return filter(bool, annexes)

    def view_conclusions(self, conclusions):
        if admin_perm.can() or expert_perm.can():
            return conclusions
        conclusions = list(conclusions)
        ok_conclusions = filter(lambda c: c.decision in ['OK', 'END'],
                                conclusions)
        user_or_expert = (
            lambda c:
            not c.user.has_role('admin') and not c.user.has_role('expert')
            if c.user else False
        )
        user_iurmax = (
            lambda c:
            not c.user.has_role('expert')
            if c.user else False
        )
        if ok_conclusions:
            return ok_conclusions + filter(user_or_expert, conclusions)
        else:
            return filter(user_iurmax, conclusions)


class SpeciesSummary(SpeciesMixin, Summary):

    template_name = 'summary/species.html'
    manual_form_cls = SummaryManualFormSpecies
    manual_form_sta_cls = SummaryManualFormSpeciesSTA
    manual_form_ref_cls = SummaryManualFormSpeciesRef
    manual_form_ref_sta_cls = SummaryManualFormSpeciesRefSTA

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}
        if subject:
            filter_args['assesment_speciesname'] = subject
        else:
            return False
        self.restricted_countries = [r[0] for r in db.session.query(
            t_restricted_species.c.eu_country_code).
            filter(t_restricted_species.c.assesment_speciesname ==
                   subject.lower()).
            filter(t_restricted_species.c.ext_dataset_id == period).
            filter(t_restricted_species.c.show_data == 0).all()]
        if region:
            filter_args['region'] = region
        if filter_args:
            filter_args['dataset_id'] = period
            self.objects = self.model_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_cls.region, self.model_cls.country)
            self.auto_objects = (
                self.model_auto_cls.query
                .filter_by(**filter_args)
                .join(
                    EtcDicMethod,
                    self.model_auto_cls.assessment_method == EtcDicMethod.method
                )
            ).order_by(EtcDicMethod.order)
            self.manual_objects = self.model_manual_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_manual_cls.decision.desc())
        return True

    def get_context(self):
        return {
            'groups_url': url_for('common.species-groups'),
            'subjects_url': url_for('.species-summary-species'),
            'regions_url': url_for('.species-summary-regions'),
            'comments_endpoint': 'comments.species-comments',
            'edit_endpoint': '.species-summary',
            'delete_endpoint': '.species-delete',
            'update_endpoint': '.species-update',
            'datasheet_url': url_for('wiki.datasheet',
                                     page='species',
                                     subject=request.args.get('subject'),
                                     region=request.args.get('region'),
                                     period=request.args.get('period')),
            'audittrail_url': url_for('wiki.audittrail',
                                      page='species',
                                      subject=request.args.get('subject'),
                                      region=request.args.get('region'),
                                      period=request.args.get('period')),
            'audittrail_merged_url': url_for(
                'wiki.audittrail-merged',
                page='species',
                subject=request.args.get('subject'),
                region=request.args.get('region'),
                period=request.args.get('period')),
            'progress_endpoint': 'progress.species-progress',
        }

    def get_default_values(self):
        values = self.get_best_automatic()
        return values


class HabitatSummary(HabitatMixin, Summary):

    template_name = 'summary/habitat.html'
    manual_form_cls = SummaryManualFormHabitat
    manual_form_sta_cls = SummaryManualFormHabitatSTA
    manual_form_ref_cls = SummaryManualFormHabitatRef
    manual_form_ref_sta_cls = SummaryManualFormHabitatRefSTA

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}

        if subject:
            filter_args['habitatcode'] = subject
        else:
            return False
        if region:
            filter_args['region'] = region
        if filter_args:
            filter_args['dataset_id'] = period
            self.objects = self.model_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_cls.region, self.model_cls.country)
            self.auto_objects = self.model_auto_cls.query.filter_by(
                **filter_args
            )
            self.manual_objects = self.model_manual_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_manual_cls.decision.desc())
        return True

    def get_context(self):
        return {
            'groups_url': url_for('common.habitat-groups'),
            'subjects_url': url_for('.habitat-summary-species'),
            'regions_url': url_for('.habitat-summary-regions'),
            'comments_endpoint': 'comments.habitat-comments',
            'edit_endpoint': '.habitat-summary',
            'delete_endpoint': '.habitat-delete',
            'update_endpoint': '.habitat-update',
            'datasheet_url': url_for('wiki.datasheet',
                                     page='habitat',
                                     subject=request.args.get('subject'),
                                     region=request.args.get('region'),
                                     period=request.args.get('period')),
            'audittrail_url': url_for('wiki.audittrail',
                                      page='habitat',
                                      subject=request.args.get('subject'),
                                      region=request.args.get('region'),
                                      period=request.args.get('period')),
            'audittrail_merged_url': url_for(
                'wiki.audittrail-merged',
                page='habitat',
                subject=request.args.get('subject'),
                region=request.args.get('region'),
                period=request.args.get('period')),
            'progress_endpoint': 'progress.habitat-progress',
        }

    def get_default_values(self):
        values = self.get_best_automatic()
        return values

    def get_current_selection(self, period_name, group, subject, region):
        selection = super(HabitatSummary, self).get_current_selection(
            period_name, group, subject, region
        )
        if not selection:
            return selection
        details = self.get_subject_details(subject)
        if details:
            selection[2] = details.habcode + ' ' + details.name
        return selection


summary.add_url_rule('/species/summary/',
                     view_func=SpeciesSummary.as_view('species-summary'))

summary.add_url_rule('/habitat/summary/',
                     view_func=HabitatSummary.as_view('habitat-summary'))


@summary.route('/species/summary/species', endpoint='species-summary-species')
def _species():
    period, group = request.args['period'], request.args['group']
    data = SpeciesMixin.get_subjects(period, group)
    return jsonify(data)


@summary.route('/species/summary/regions', endpoint='species-summary-regions')
def _regions():
    period, subject = request.args['period'], request.args['subject']
    data = SpeciesMixin.get_regions(period, subject)
    return jsonify(data)


@summary.route('/species/summary/countries', endpoint='species-summary-countries')
def _countries():
    period, group = request.args['period'], request.args['group']
    data = SpeciesMixin.get_countries(period, group)
    return jsonify(data)


@summary.route('/habitat/summary/habitat', endpoint='habitat-summary-species')
def _species_habitat():
    period, group = request.args['period'], request.args['group']
    data = HabitatMixin.get_subjects(period, group)
    return jsonify(data)


@summary.route('/habitat/summary/regions', endpoint='habitat-summary-regions')
def _regions_habitat():
    period, subject = request.args['period'], request.args['subject']
    data = HabitatMixin.get_regions(period, subject)
    return jsonify(data)


class MixinView(object):

    def __init__(self, mixin):
        self.mixin = mixin


class ConclusionDelete(MixinView, views.View):

    def dispatch_request(self):
        period = request.args.get('period')
        subject = request.args.get('subject')
        region = request.args.get('region')
        delete_region = request.args.get('delete_region')
        delete_user = request.args.get('delete_user')
        delete_ms = request.args.get('delete_ms')
        record = self.mixin.get_manual_record(period, subject, delete_region,
                                              delete_user, delete_ms)
        if not record:
            abort(404)
        if not can_delete(record):
            abort(403)
        if record.deleted:
            record.deleted = 0
        else:
            record.deleted = 1
        db.session.add(record)
        db.session.commit()
        return redirect(
            url_for(self.mixin.summary_endpoint, period=period,
                    subject=subject, region=region)
        )


summary.add_url_rule('/species/conc/delete/',
                     view_func=ConclusionDelete
                     .as_view('species-delete', mixin=SpeciesMixin))
summary.add_url_rule('/habitat/conc/delete/',
                     view_func=ConclusionDelete
                     .as_view('habitat-delete', mixin=HabitatMixin))


class UpdateDecision(MixinView, views.View):

    methods = ['GET', 'POST']

    def dispatch_request(self, period, subject, region, user, ms):
        self.record = self.mixin.get_manual_record(period, subject, region,
                                                   user, ms)
        if not self.record:
            abort(404)

        if not can_update_decision(self.record):
            abort(403)

        if not request.form.get('decision'):
            abort(401)

        decision = request.form['decision']
        result = self.validate(decision)
        if result['success']:
            self.record.decision = decision
            self.record.last_update = datetime.now().strftime(DATE_FORMAT_PH)
            db.session.commit()
        return jsonify(result)

    def validate(self, decision):
        validation_values = ['OK', 'END']
        if decision == 'OK?':
            return {
                'success': False,
                'error': "You are not allowed to select 'OK?'" +
                         "Please select another value."
            }
        elif decision in validation_values:
            for r in self.get_sister_records(self.record):
                if r.decision in validation_values:
                    return {
                        'success': False,
                        'error': "Another final decision already exists",
                    }

        return {'success': True}

    def get_sister_records(self, record):
        return (
            self.mixin.model_manual_cls.query
            .filter_by(subject=record.subject, region=record.region,
                       dataset_id=record.dataset_id)
            .filter(~(self.mixin.model_manual_cls.user == record.user))
        )


summary.add_url_rule('/species/conc/update/<period>/<subject>/<region>/<user>/<ms>/',
                     view_func=UpdateDecision
                     .as_view('species-update', mixin=SpeciesMixin))
summary.add_url_rule('/habitat/conc/update/<period>/<subject>/<region>/<user>/<ms>/',
                     view_func=UpdateDecision
                     .as_view('habitat-update', mixin=HabitatMixin))
