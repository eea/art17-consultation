from flask_principal import Permission, RoleNeed
from art17.models import (
    EtcDataSpeciesAutomaticAssessment,
    EtcDataHabitattypeAutomaticAssessment,
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


def get_default_period():
    return '1'


admin_perm = Permission(RoleNeed('admin'))
expert_perm = Permission(RoleNeed('expert'))


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


