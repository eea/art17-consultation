# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from datetime import date
import flask
from flask_principal import Permission, RoleNeed
from art17.dataset import CONVERTER_URLS
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import (
    db,
    Dataset,
    EtcDataSpeciesAutomaticAssessment,
    EtcDataHabitattypeAutomaticAssessment,
    EtcDataSpeciesRegion,
    EtcDataHabitattypeRegion,
    Config,
    restricted_species_2013,
)

from .utils import str2num


DATE_FORMAT = '%Y-%m-%d %H:%M'
DEFAULT_MS = 'EU28'

QUALITIES = {
    'B': 'Bad',
    'P': 'Poor',
    'G': 'Good',
    'M': 'Moderate',
    'U': 'Unkown',
}

CONCLUSION_CLASSES = {
    'FV': 'FV',
    'U1': 'U1',
    'U1-': 'U1M',
    'U1+': 'U1P',
    'U2': 'U2',
    'U2-': 'U2M',
    'U2+': 'U2P',
    'XX': 'XX',
    'NA': 'NA',
    'XU': 'XU',
    'U2?': 'U2U',
    'U1?': 'U1U',
    'FV?': 'FVU',
    'XX?': 'XXU',
    'XU?': 'XUU',
}

COUNTRY_ASSESSMENTS = {
    'FV':  'Favourable (FV)',
    'U1':  'Inadequate (U1)',
    'U1-': 'Inadequate and deteriorating (U1-)',
    'U1+': 'Inadequate but improving (U1+)',
    'U2':  'Bad (U2)',
    'U2-': 'Bad and deteriorating (U2-)',
    'U2+': 'Bad but improving (U2+)',
    'XX':  'Unknown (XX)',
    'NA':  'Imposible to be assesed',
}

CONTRIB_METHOD = {
    'A': 'favorable',
    'B': 'improvement',
    'C': 'deterioration',
    'D': 'same',
    'E': 'unknown',
}

CONTRIB_CONCLUSION = {
    '+': 'improvement',
    '-': 'deterioration',
    '0': 'no change',
    'x': 'not known',
}

TREND_OPTIONS = [
    ('x', 'unknown'),
    ('0', 'stable'),
    ('+', 'increase'),
    ('-', 'decrease'),
    ('N/A', 'not reported'),
]

TREND_OPTIONS_OVERALL = [
    ('x', 'unknown'),
    ('=', 'stable'),
    ('+', 'imporving'),
    ('-', 'declining'),
    ('N/A', 'not reported'),
]

NATURE_OF_CHANGE_OPTIONS = [
    ('a', 'genuine change'),
    ('b1', 'more accurate'),
    ('b2', 'taxonomic review'),
    ('c1', 'use of different methods to measure or evaluate individual ' +
           'parameters in overall conservation status'),
    ('c2', 'use of different thresholds'),
    ('d', 'no information about the nature of change'),
    ('e', 'less accurate data than those used in the previous reporting ' +
          'or absent data'),
    ('nc', 'no change'),
    ('N/A', 'not reported'),
]

HABITAT_OPTIONS = [
    ('g', 'good'),
    ('m', 'moderate'),
    ('b', 'bad'),
    ('u', 'unknown'),
    ('N/A', 'not reported'),
]

FAV_REF_OPTIONS = {
    'complementary_favourable_range': [
        ('>', 'more than current value'),
        ('>>', 'much more than current value'),
        ('x', 'unknown')],
    'common': [
        ('>', 'more than current value'),
        ('>>', 'much more than current value'),
        ('<', 'less than current value'),
        ('x', 'unknown')],
    '2006': [(u'~', 'approximately equal to current value')],
    '2012': [(u'≈', 'approximately equal to current value')]
}

MANUAL_TOOLTIPS = {
    'method_range': 'percentage_range_surface_area',
    'method_population': 'percentage_population_mean_size',
    'method_future': 'percentage_future',
    'method_habitat': 'percentage_habitat_surface_area',
    'method_assessment': 'percentage_assessment',
    'method_area': 'percentage_coverage_surface_area',
    'method_structure': 'percentage_structure',
}

HOMEPAGE_VIEW_NAME = 'common.homepage'

common = flask.Blueprint('common', __name__)


def get_config():
    rows = Config.query.all()
    if len(rows) != 1:
        raise RuntimeError("There should be exactly one config row")
    return rows[0]


def get_default_period():
    conf = get_config()
    return conf.default_dataset_id


def consultation_ended():
    cfg = get_config()
    if cfg.end_date:
        today = date.today()
        return cfg.end_date < today
    return False


@common.app_template_global('sta_cannot_change')
def sta_cannot_change():
    return sta_perm.can() and consultation_ended()


admin_perm = Permission(RoleNeed('admin'))
sta_perm = Permission(RoleNeed('stakeholder'))
etc_perm = Permission(RoleNeed('etc'))
nat_perm = Permission(RoleNeed('nat'))


def is_public_user():
    """ Call for authenticated users. """
    return not (
        admin_perm.can() or sta_perm.can() or etc_perm.can() or nat_perm.can()
    )


@common.record
def register_permissions_in_template_globals(state):
    app = state.app

    app.jinja_env.globals['admin_perm'] = admin_perm
    app.jinja_env.globals['etc_perm'] = etc_perm
    app.jinja_env.globals['sta_perm'] = sta_perm
    app.jinja_env.globals['nat_perm'] = nat_perm
    app.jinja_env.globals['HOMEPAGE_VIEW_NAME'] = HOMEPAGE_VIEW_NAME
    app.jinja_env.globals['DEMO_SERVER'] = app.config.get('DEMO_SERVER', True)
    app.jinja_env.globals['SCRIPT_NAME'] = app.config.get('SCRIPT_NAME',
                                                          '/article17')
    app.jinja_env.globals['EEA_PASSWORD_RESET'] = app.config.get(
        'EEA_PASSWORD_RESET', ''
    )


@common.app_context_processor
def inject_globals():
    from art17.auth import current_user

    cfg = get_config()

    today = date.today()
    if cfg.start_date:
        if cfg.end_date:
            consultation_started = cfg.start_date <= today <= cfg.end_date
        else:
            consultation_started = cfg.start_date <= today
    else:
        consultation_started = False
    is_public = not current_user.is_authenticated or is_public_user()

    return {
        'APP_BREADCRUMBS': [
            ('Article 17', flask.url_for(HOMEPAGE_VIEW_NAME))],
        'consultation_started': consultation_started,
        'today': today,
        'start_date': cfg.start_date,
        'end_date': cfg.end_date,
        'is_public': is_public,
        'current_user': current_user,
    }


class MixinView(object):

    def __init__(self, mixin):
        self.mixin = mixin


def population_size_unit(row):

    min_size = row.population_minimum_size or ''
    max_size = row.population_maximum_size or ''
    filled = row.filled_population or 'N/A'
    size_unit = row.population_size_unit or 'N/A'

    if filled == 'Min':
        min_size = '(%s)' % min_size
    if filled == 'Max':
        max_size = '(%s)' % max_size

    if min_size or max_size:
        size_unit_value = '%s - %s' % (min_size, max_size)
    else:
        size_unit_value = 'N/A'

    return '%s %s' % (str2num(size_unit_value), size_unit)


def population_size_unit_title(row, ds_schema):
    titles = []
    reason, agreed, other = '', '', ''
    if ds_schema == '2006':
        reason, agreed, other = 'Reason for change: ', 'Agreed: ', 'Other: '
    elif ds_schema == '2012':
        reason, agreed, other = (
            'Reason for change if current value is different than in 2007: ',
            'Agreed units: ', 'Alternative units: ')
    titles.append(reason + (row.population_change_reason or 'N/A'))
    titles.append(agreed + (row.population_units_agreed or 'N/A'))
    titles.append(other + (row.population_units_other or 'N/A'))
    if not titles:
        return ''
    return '\n'.join(titles)


def population_ref(row):

    population_q = row.complementary_favourable_population_q or ''
    population = row.complementary_favourable_population
    filled = row.filled_complementary_favourable_population or ''

    if not (population_q or population):
        return 'N/A'

    content = '%s(%s)' if filled else '%s%s'
    return content % (population_q, str2num(population, ''))


def favourable_ref_title(field, schema):
    text_lines = ['Favourable reference value: ']
    if field in ('complementary_favourable_range',
                 'complementary_favourable_area'):
        text_lines.append('(if only operator was used in MS data current value'
                          ' was inserted automatically)')
    elif field == 'complementary_favourable_population':
        text_lines.append('(if only operator was used in MS data current value'
                          '(min) was inserted automatically)')
    return text_lines


def favourable_ref_title_habitat(field, schema):
    text_lines = favourable_ref_title(field, schema)
    options = FAV_REF_OPTIONS['common'][:-1] + \
        FAV_REF_OPTIONS.get(schema, []) + FAV_REF_OPTIONS['common'][-1:]
    text_lines.extend([' '.join(opt) for opt in options])
    return '\n'.join(text_lines)


def favourable_ref_title_species(field, schema):
    text_lines = favourable_ref_title(field, schema)
    options = FAV_REF_OPTIONS.get(field, FAV_REF_OPTIONS['common'])[:-1] + \
        FAV_REF_OPTIONS.get(schema, []) + \
        FAV_REF_OPTIONS.get(field, FAV_REF_OPTIONS['common'])[-1:]
    text_lines.extend([' '.join(opt) for opt in options])
    return '\n'.join(text_lines)


def get_tooltip(row, method_field, model_auto_cls):
    tooltip_field = MANUAL_TOOLTIPS.get(method_field, '')
    if not tooltip_field:
        return ''
    query = (
        model_auto_cls.query
        .with_entities(
            getattr(model_auto_cls, tooltip_field))
        .filter_by(subject=row.subject,
                   region=row.region,
                   assessment_method=getattr(row, method_field),
                   dataset_id=row.dataset_id)
        .first()
    )
    return getattr(query, tooltip_field) if query else ''


def get_tooltip_for_species(row, method_field):
    return get_tooltip(row, method_field, EtcDataSpeciesAutomaticAssessment)


def get_tooltip_for_habitat(row, method_field):
    return get_tooltip(row, method_field, EtcDataHabitattypeAutomaticAssessment)


def get_original_record_url(row):
    if isinstance(row, EtcDataSpeciesRegion):
        page = 'species'
        code = row.speciescode
    elif isinstance(row, EtcDataHabitattypeRegion):
        page = 'habitat'
        code = row.habitatcode
    else:
        raise NotImplementedError

    if row.eu_country_code in ['EL', 'GR'] and row.dataset.schema != '2018':
        schema = '2006'
    elif row.dataset:
        schema = row.dataset.schema
    else:
        schema = 0
    if schema == '2018':
        return '{}#{}'.format(row.filename, code)
    url_scheme = CONVERTER_URLS.get(schema, {})
    url_format = url_scheme.get(page, '')
    info = urlparse(row.envelope)
    url_form = url_format.format(
        scheme=info.scheme, host=info.netloc, path=info.path,
        filename=row.filename,
        region=row.region,
        subject=row.speciescode if page == 'species' else row.habitatcode,
    )
    return url_form


def get_title_for_species_country(row):
    s_name, s_info, s_type = '', '', ''
    if (row.speciesname != row.assesment_speciesname or
            row.complementary_other_information):
        s_name = row.speciesname or row.assesment_speciesname or ''
        s_info = row.complementary_other_information or ''
    if row.species_type_asses == 0:
        s_type = row.species_type_details.SpeciesType \
            if row.species_type_details else row.species_type
    if s_info:
        s_info = 'Information provided in the field 2.8.2: ' + s_info.replace(
            '\n', '<br/>')
    return s_name, s_info, s_type


def get_title_for_habitat_country(row):
    s_name, s_info, s_type = '', '', ''
    if row.complementary_other_information:
        s_info = row.complementary_other_information or ''
    if row.habitattype_type_asses == 0:
        s_type = row.habitattype_type_details.SpeciesType \
            if row.habitattype_type_details else row.habitattype_type
    if s_info:
        s_info = 'Information provided in the field 2.7.5: ' + s_info.replace(
            '\n', '<br/>')
    return s_name, s_info, s_type


def generate_map_url(dataset_id, category, subject, region, sensitive=False):
    dataset = Dataset.query.get(dataset_id)
    if category == 'species':
        field_2018 = 'speciescode'
        if sensitive:
            map_href = dataset.sensitive_species_map_url
        else:
            map_href = dataset.species_map_url

    elif category == 'habitat':
        field_2018 = 'habitatcode'
        map_href = dataset.habitat_map_url

    else:
        raise RuntimeError('unknown category %r' % category)

    if not map_href:
        return ''

    if region:
        if dataset.schema == '2018':
            return "&".join([map_href, field_2018 + "=" + subject, 'region' + "=" + region])
        else:
            return map_href + '&CodeReg=' + subject + region
    else:
        if dataset.schema == '2018':
            return "&".join([map_href, field_2018 + "=" + subject, 'region=%25'])
        else:
            return map_href + '&CCode=' + subject


@common.app_template_global('is_sensitive')
def get_sensitive_records(speciescode=''):
    return (
        db.session.query(restricted_species_2013)
        .filter_by(speciescode=speciescode)
        .all()
    )


@common.route('/')
def homepage():
    from art17.auth import current_user

    return flask.render_template('homepage.html', **{
        'current_user': current_user,
    })


@common.route('/_crashme', methods=['GET', 'POST'])
def crashme():
    if flask.request.method == 'POST':
        raise RuntimeError("Crashing as requested")
    return '<form method="post"><button type="submit">crash</button></form>'


@common.route('/_ping')
def ping():
    return 'hello world: %d' % Config.query.count()


@common.route('/common/species/groups', endpoint='species-groups')
def species_groups():
    data = SpeciesMixin.get_groups(flask.request.args['period'])
    return flask.jsonify([list(row) for row in data])


@common.route('/common/habitat/groups', endpoint='habitat-groups')
def habitat_groups():
    from art17.progress import HabitatProgressTable
    if flask.request.args.get('table_view'):
        data = HabitatProgressTable.get_groups(flask.request.args['period'])
    else:
        data = HabitatMixin.get_groups(flask.request.args['period'])
    return flask.jsonify([list(row) for row in data])


@common.route('/config', methods=['GET', 'POST'])
def config():
    from art17.forms import ConfigForm
    admin_perm.test()
    row = get_config()
    form = ConfigForm(flask.request.form, obj=row)

    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        flask.flash("Configuration saved", 'success')
        return flask.redirect(flask.url_for('.config'))

    return flask.render_template('config.html', form=form)


@common.route('/auth/details', methods=['GET', 'POST'])
def change_details():
    from art17.auth import current_user

    if current_user.is_anonymous:
        flask.flash('You need to login to access this page.')
        return flask.redirect(flask.url_for(HOMEPAGE_VIEW_NAME))
    else:
        from art17.forms import ChangeDetailsForm
        form = ChangeDetailsForm(flask.request.form, obj=current_user)
        if form.validate_on_submit():
            flask.flash('Details updated successfully!', 'success')
            form.populate_obj(current_user)
            role = form.data['role']
            if role:
                datastore = flask.current_app.extensions['security'].datastore
                datastore.add_role_to_user(current_user, role)
                current_user_roles = [r.name for r in current_user.roles]
                expandable_roles = filter(lambda k: k not in [role], current_user_roles)
                for role in expandable_roles:
                    datastore.remove_role_from_user(current_user, role)
                datastore.commit()
            db.session.commit()

    return flask.render_template('change_details.html', form=form)


@common.app_template_filter('ugly_fix')
def ugly_fix(value):
    return value.replace('art17.eionet', 'bd.eionet')
