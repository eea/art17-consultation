# -*- coding: utf-8 -*-
from urlparse import urlparse
from datetime import date
import flask
from flask_principal import Permission, RoleNeed
from art17.dataset import CONVERTER_URLS
from art17.mixins import SpeciesMixin, HabitatMixin
from art17.models import (
    db,
    EtcDataSpeciesAutomaticAssessment,
    EtcDataHabitattypeAutomaticAssessment,
    EtcDataSpeciesRegion,
    EtcDataHabitattypeRegion,
    Config,
)

from .utils import str2num

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
    'common': [
        ('>', 'more than current value'),
        ('>>', 'much more than current value'),
        ('<', 'less than current value'),
        ('x', 'unknown')],
    '2006': [(u'~', 'approximately equal to current value')],
    '2012': [(u'≈', 'approximately equal to current value')]
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


admin_perm = Permission(RoleNeed('admin'))
sta_perm = Permission(RoleNeed('stakeholder'))
etc_perm = Permission(RoleNeed('etc'))
nat_perm = Permission(RoleNeed('nat'))


@common.record
def register_permissions_in_template_globals(state):
    app = state.app

    app.jinja_env.globals['admin_perm'] = admin_perm
    app.jinja_env.globals['etc_perm'] = etc_perm
    app.jinja_env.globals['sta_perm'] = sta_perm
    app.jinja_env.globals['HOMEPAGE_VIEW_NAME'] = HOMEPAGE_VIEW_NAME
    app.jinja_env.globals['DEMO_SERVER'] = app.config.get('DEMO_SERVER', True)


@common.app_context_processor
def inject_globals():
    return {
        'APP_BREADCRUMBS': [('Article 17', flask.url_for(HOMEPAGE_VIEW_NAME))],
    }


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
    options = FAV_REF_OPTIONS['common'][:-1] + \
        FAV_REF_OPTIONS.get(schema, []) + FAV_REF_OPTIONS['common'][-1:]
    text_lines.extend([' '.join(opt) for opt in options])
    return '\n'.join(text_lines)


def get_range_conclusion_value(assesment_speciesname, region,
                               assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(
            EtcDataSpeciesAutomaticAssessment.percentage_range_surface_area)
        .filter_by(assesment_speciesname=assesment_speciesname, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_range_surface_area if query else ''


def get_population_conclusion_value(assesment_speciesname, region,
                                    assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(
            EtcDataSpeciesAutomaticAssessment.percentage_population_mean_size)
        .filter_by(assesment_speciesname=assesment_speciesname, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_population_mean_size if query else ''


def get_future_conclusion_value_for_species(assesment_speciesname, region,
                                            assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(
            EtcDataSpeciesAutomaticAssessment.percentage_future)
        .filter_by(assesment_speciesname=assesment_speciesname,
                   region=region,
                   assessment_method=assessment_method)
        .first()
    )

    return query.percentage_future if query else ''


def get_habitat_conclusion_value(assesment_speciesname, region,
                                 assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(
            EtcDataSpeciesAutomaticAssessment.percentage_habitat_surface_area)
        .filter_by(assesment_speciesname=assesment_speciesname,
                   region=region,
                   assessment_method=assessment_method)
        .first()
    )

    return query.percentage_habitat_surface_area if query else ''


def get_future_conclusion_value_for_habitat(habitatcode, region,
                                            assessment_method):
    query = (
        EtcDataHabitattypeAutomaticAssessment.query
        .with_entities(EtcDataHabitattypeAutomaticAssessment.percentage_future)
        .filter_by(habitatcode=habitatcode,
                   region=region,
                   assessment_method=assessment_method)
        .first()
    )

    return query.percentage_future if query else ''


def get_assesm_conclusion_value_for_species(assesment_speciesname, region,
                                            assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(EtcDataSpeciesAutomaticAssessment.percentage_assessment)
        .filter_by(assesment_speciesname=assesment_speciesname,
                   region=region,
                   assessment_method=assessment_method)
        .first()
    )

    return query.percentage_assessment if query else ''


def get_assesm_conclusion_value_for_habitat(habitatcode, region,
                                            assessment_method):
    query = (
        EtcDataHabitattypeAutomaticAssessment.query
        .with_entities(
            EtcDataHabitattypeAutomaticAssessment.percentage_assessment)
        .filter_by(habitatcode=habitatcode,
                   region=region,
                   assessment_method=assessment_method)
        .first()
    )

    return query.percentage_assessment if query else ''


def get_coverage_conclusion_value(habitatcode, region, assessment_method):
    query = (
        EtcDataHabitattypeAutomaticAssessment.query
        .filter_by(habitatcode=habitatcode, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_coverage_surface_area if query else ''


def get_struct_conclusion_value(habitatcode, region, assessment_method):
    query = (
        EtcDataHabitattypeAutomaticAssessment.query
        .with_entities(
            EtcDataHabitattypeAutomaticAssessment.percentage_structure)
        .filter_by(habitatcode=habitatcode, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_structure if query else ''


def get_original_record_url(row):
    if isinstance(row, EtcDataSpeciesRegion):
        page = 'species'
    elif isinstance(row, EtcDataHabitattypeRegion):
        page = 'habitat'
    else:
        raise NotImplementedError
    url_scheme = CONVERTER_URLS.get(row.dataset.schema if row.dataset else 0, {})
    url_format = url_scheme.get(page, '')
    info = urlparse(row.envelope)
    return url_format.format(
        scheme=info.scheme, host=info.netloc, path=info.path,
        filename=row.filename,
        region=row.region,
        subject=row.speciescode if page == 'species' else row.habitatcode,
    )


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


@common.route('/')
def homepage():
    cfg = get_config()
    from art17.auth.security import current_user

    return flask.render_template('homepage.html', **{
        'start_date': cfg.start_date,
        'end_date': cfg.end_date,
        'today': date.today(),
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
    return flask.jsonify(data)


@common.route('/common/habitat/groups', endpoint='habitat-groups')
def habitat_groups():
    data = HabitatMixin.get_groups(flask.request.args['period'])
    return flask.jsonify(data)


@common.route('/config', methods=['GET', 'POST'])
def config():
    from art17.forms import ConfigForm
    admin_perm.test()
    row = get_config()
    form = ConfigForm(flask.request.form, row)

    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        flask.flash("Configuration saved", 'success')
        return flask.redirect(flask.url_for('.config'))

    return flask.render_template('config.html', form=form)
