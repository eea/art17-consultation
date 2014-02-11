from urlparse import urlparse
import flask
from flask_principal import Permission, RoleNeed
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
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
    'P': 'Poor',
    'G': 'Good',
    'M': 'Moderate',
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

HOMEPAGE_VIEW_NAME = 'summary.homepage'

common = flask.Blueprint('common', __name__)


def get_default_period():
    return '1'


admin_perm = Permission(RoleNeed('admin'))
expert_perm = Permission(RoleNeed('expert'))
sta_perm = Permission(RoleNeed('stakeholder'))
etc_perm = Permission(RoleNeed('etc'))

@common.record
def register_permissions_in_template_globals(state):
    app = state.app

    app.jinja_env.globals['admin_perm'] = admin_perm
    app.jinja_env.globals['expert_perm'] = expert_perm


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


def population_size_unit_title(row):
    titles = []
    if row.population_change_reason:
        titles.append(row.population_change_reason)
    titles.append("Agreed: " + (row.population_units_agreed or 'N/A'))
    titles.append("Other: " + (row.population_units_other or 'N/A'))
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


def get_range_conclusion_value(assesment_speciesname, region,
                               assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(EtcDataSpeciesAutomaticAssessment.percentage_range_surface_area)
        .filter_by(assesment_speciesname=assesment_speciesname, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_range_surface_area if query else ''


def get_population_conclusion_value(assesment_speciesname, region,
                                    assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(EtcDataSpeciesAutomaticAssessment.percentage_population_mean_size)
        .filter_by(assesment_speciesname=assesment_speciesname, region=region,
                   assessment_method=assessment_method)
        .first()
    )
    return query.percentage_population_mean_size if query else ''


def get_future_conclusion_value_for_species(assesment_speciesname, region,
                                            assessment_method):
    query = (
        EtcDataSpeciesAutomaticAssessment.query
        .with_entities(EtcDataSpeciesAutomaticAssessment.percentage_future)
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
        .with_entities(EtcDataSpeciesAutomaticAssessment.percentage_habitat_surface_area)
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
        .with_entities(EtcDataHabitattypeAutomaticAssessment.percentage_assessment)
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
        .with_entities(EtcDataHabitattypeAutomaticAssessment.percentage_structure)
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
    title = []
    if (row.speciesname != row.assesment_speciesname or
        row.complementary_other_information != ''):
        title.append('\"%s\"\n%s' % (row.speciesname, row.complementary_other_information))
        if row.species_type_asses == 0:
            title.append('\n\n%s' % (row.species_type_details.SpeciesType
                         if row.species_type_details else row.species_type))
        title.append('\n\nClick to open original report in a new window')
    elif row.species_type_asses == 0:
            title.append(row.species_type_details.SpeciesType
                         if row.species_type_details else row.species_type)
    else:
        title.append('Click to open original report in a new window')

    return title


def get_title_for_habitat_country(row):
    title = []
    if row.complementary_other_information != '':
        title.append('%s' % row.complementary_other_information)
        if row.habitattype_type_asses == 0:
            title.append('\n\n%s' % (row.habitattype_type_details.SpeciesType
                         if row.habitattype_type_details else row.habitattype_type))
        title.append('\n\nClick to open original report in a new window')
    elif row.habitattype_type_asses == 0:
            title.append('\n\n%s' % (row.habitattype_type_details.SpeciesType
                         if row.habitattype_type_details else row.habitattype_type))
    else:
        title.append('Click to open original report in a new window')

    return title


@common.route('/common/species/groups', endpoint='species-groups')
def species_groups():
    data = SpeciesMixin.get_groups(flask.request.args['period'])
    return flask.jsonify(data)


@common.route('/common/habitat/groups', endpoint='habitat-groups')
def habitat_groups():
    data = HabitatMixin.get_groups(flask.request.args['period'])
    return flask.jsonify(data)


def get_config():
    rows = Config.query.all()
    if len(rows) != 1:
        raise RuntimeError("There should be exactly one config row")
    return rows[0]


ConfigForm = model_form(Config, base_class=Form, field_args={
        'start_date': {'label': "Start date (YYYY-MM-DD)"},
        'end_date': {'label': "End date (YYYY-MM-DD)"},
        'admin_email': {'label': "Administrator email (space separated list)"},
    })


@common.route('/config', methods=['GET', 'POST'])
def config():
    admin_perm.test()
    row = get_config()
    form = ConfigForm(flask.request.form, row)

    if form.validate_on_submit():
        form.populate_obj(row)
        db.session.commit()
        flask.flash("Configuration saved", 'success')
        return flask.redirect(flask.url_for('.config'))

    return flask.render_template('config.html', form=form)
