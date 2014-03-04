from datetime import datetime
from flask import (
    views,
    request,
    render_template,
    jsonify,
    url_for,
    flash,
    g,
)
from flask.ext.principal import PermissionDenied
from sqlalchemy import and_
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
)
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.common import (
    get_default_period,
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
    population_size_unit_title,
    favourable_ref_title,
    CONCLUSION_CLASSES,
    COUNTRY_ASSESSMENTS,
    QUALITIES,
    CONTRIB_METHOD,
    CONTRIB_CONCLUSION,
    TREND_OPTIONS, TREND_OPTIONS_OVERALL, NATURE_OF_CHANGE_OPTIONS,
    HABITAT_OPTIONS,
    etc_perm,
    nat_perm,
    get_config,
)
from art17.forms import (
    SummaryFilterForm,
    SummaryManualFormSpecies,
    SummaryManualFormHabitat,
    SummaryManualFormHabitatRef,
    SummaryManualFormSpeciesRef,
    SummaryManualFormSpeciesSTA,
    SummaryManualFormSpeciesRefSTA,
    SummaryManualFormHabitatRefSTA,
    SummaryManualFormHabitatSTA,
)
from art17.utils import str2num, parse_semicolon, str1num, na_if_none
from art17.summary.permissions import can_touch, must_edit_ref
from art17.summary import summary
from art17.summary.conclusion import (
    UpdateDecision,
    ConclusionDelete,
    ConclusionView,
)
from art17.comments import SpeciesCommentCounter, HabitatCommentCounter


DATE_FORMAT = '%d/%m/%Y %H:%M'


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
        'get_future_conclusion_value_for_species':
            get_future_conclusion_value_for_species,
        'get_future_conclusion_value_for_habitat':
            get_future_conclusion_value_for_habitat,
        'get_assesm_conclusion_value_for_species':
            get_assesm_conclusion_value_for_species,
        'get_assesm_conclusion_value_for_habitat':
            get_assesm_conclusion_value_for_habitat,
        'get_habitat_conclusion_value': get_habitat_conclusion_value,
        'get_coverage_conclusion_value': get_coverage_conclusion_value,
        'get_struct_conclusion_value': get_struct_conclusion_value,
        'get_original_record_url': get_original_record_url,
        'favourable_ref_title': favourable_ref_title,
    }


@summary.app_context_processor
def inject_static():
    make_tooltip = lambda d: '\n' + '\n'.join(['%s: %s' % (k, v) for k, v in d])
    return {
        'etc_perm': etc_perm,
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


@summary.app_template_filter('na_if_none')
def _na_if_none(value, default='N/A'):
    return na_if_none(value, default=default)


@summary.app_template_filter('get_quality')
def get_quality(value, default='N/A'):
    if value and value[0].upper() in QUALITIES:
        return value[0]
    return default if not value else value[0]


@summary.app_template_filter('format_date')
def format_date(value):
    if not value:
        return ''
    try:
        date_value = datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return value
    return date_value.strftime('%m/%y')


@summary.app_template_filter('format_units')
def format_units(value):
    if value and value[-2:] == ' i':
        return value[:-2] + ' indiv.'
    return value


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


def parse_qa_errors(fields, record, qa_errors):
    title = []
    classes = []
    if isinstance(fields, str):
        fields = [fields]
    for field in fields:
        if field in qa_errors:
            error = qa_errors[field]
            if error.get('suspect_value', ''):
                title.append('%s: %s' % (error['text'], error['suspect_value']))
            else:
                title.append(error['text'])
            classes.append('qa_error')
    return '<br/>'.join(title), ' '.join(classes)


class Summary(ConclusionView, views.View):

    methods = ['GET', 'POST']

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
            manual_form.region.process_data(region or manual_form.region.data)
        if hasattr(manual_form, 'MS'):
            manual_form.kwargs = dict(subject=subject, period=period)
            manual_form.MS.choices = self.get_MS(subject, region, period)

        if request.method == 'POST':
            home_url = url_for(self.summary_endpoint, period=period,
                               subject=subject, region=region)

            if manual_form.validate(subject=subject, period=period):
                if not can_touch(manual_assessment):
                    raise PermissionDenied()

                if not manual_assessment:
                    manual_assessment = self.model_manual_cls(subject=subject)
                    manual_form.populate_obj(manual_assessment)
                    manual_assessment.last_update = datetime.now().strftime(DATE_FORMAT)
                    manual_assessment.user_id = current_user.id
                    manual_assessment.dataset_id = period
                    if nat_perm.can():
                        manual_assessment.MS = current_user.MS
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
            'manual_objects': self.filter_conclusions(self.manual_objects),
            'restricted_countries': self.restricted_countries,
            'regions': regions,
            'summary_filter_form': summary_filter_form,
            'manual_form': manual_form,
            'manual_assessment': manual_assessment,
            'edit_ref': must_edit_ref(manual_assessment),
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


class SpeciesSummary(SpeciesMixin, Summary):

    template_name = 'summary/species.html'
    manual_form_cls = SummaryManualFormSpecies
    manual_form_sta_cls = SummaryManualFormSpeciesSTA
    manual_form_ref_cls = SummaryManualFormSpeciesRef
    manual_form_ref_sta_cls = SummaryManualFormSpeciesRefSTA

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}
        self.wiki_unread = (
            SpeciesCommentCounter(period, g.identity.id)
            .get_wiki_unread_count(subject, region)
        )
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
            ).order_by(self.model_cls.presence.desc(), self.model_cls.region,
                       self.model_cls.country)
            self.auto_objects = (
                self.model_auto_cls.query
                .filter_by(**filter_args)
                .join(
                    EtcDicMethod,
                    and_(self.model_auto_cls.assessment_method == EtcDicMethod.method,
                    EtcDicMethod.dataset_id == period),
                )
            ).order_by(EtcDicMethod.order)
            self.manual_objects = self.model_manual_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_manual_cls.decision.desc())
        return True

    def get_context(self):
        map_url = ''
        subject = request.args.get('subject')
        if subject:
            map_url = generate_map_url(
                category='species',
                subject=subject,
                region=request.args.get('region', ''),
            )
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
            'get_title_for_country': get_title_for_species_country,
            'wiki_unread': self.wiki_unread,
            'map_url': map_url,
        }


class HabitatSummary(HabitatMixin, Summary):

    template_name = 'summary/habitat.html'
    manual_form_cls = SummaryManualFormHabitat
    manual_form_sta_cls = SummaryManualFormHabitatSTA
    manual_form_ref_cls = SummaryManualFormHabitatRef
    manual_form_ref_sta_cls = SummaryManualFormHabitatRefSTA

    def setup_objects_and_data(self, period, subject, region):
        filter_args = {}
        self.wiki_unread = (
            HabitatCommentCounter(period, g.identity.id)
            .get_wiki_unread_count(subject, region)
        )

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
            self.auto_objects = (
                self.model_auto_cls.query
                .filter_by(**filter_args)
                .join(
                    EtcDicMethod,
                    and_(self.model_auto_cls.assessment_method == EtcDicMethod.method,
                    EtcDicMethod.dataset_id == period),
                )
            ).order_by(EtcDicMethod.order)
            self.manual_objects = self.model_manual_cls.query.filter_by(
                **filter_args
            ).order_by(self.model_manual_cls.decision.desc())
        return True

    def get_context(self):
        map_url = ''
        subject = request.args.get('subject')
        if subject:
            map_url = generate_map_url(
                category='habitat',
                subject=subject,
                region=request.args.get('region', ''),
            )
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
            'get_title_for_country': get_title_for_habitat_country,
            'wiki_unread': self.wiki_unread,
            'map_url': map_url,
        }

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


summary.add_url_rule('/species/conc/delete/',
                     view_func=ConclusionDelete
                     .as_view('species-delete', mixin=SpeciesMixin))
summary.add_url_rule('/habitat/conc/delete/',
                     view_func=ConclusionDelete
                     .as_view('habitat-delete', mixin=HabitatMixin))

summary.add_url_rule(
    '/species/conc/update/<period>/<subject>/<region>/<user>/',
    view_func=UpdateDecision
    .as_view('species-update', mixin=SpeciesMixin))
summary.add_url_rule(
    '/habitat/conc/update/<period>/<subject>/<region>/<user>/',
    view_func=UpdateDecision
    .as_view('habitat-update', mixin=HabitatMixin))


def generate_map_url(category, subject, region):
    config = get_config()
    if category == 'species':
        return (
            (config.species_map_url or '')
            .replace("{species}", subject)
            .replace("{region}", region)
        )

    if category == 'habitat':
        return (
            (config.habitat_map_url or '')
            .replace("{habitat}", subject)
            .replace("{region}", region)
        )

    raise RuntimeError('unknown category %r' % category)
