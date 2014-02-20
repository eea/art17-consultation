import pytest

from art17.models import db
from .factories import (
    EtcDataSpeciesRegionFactory,
    SpeciesManualAssessmentFactory,
    EtcDataSpeciesAutomaticAssessmentFactory,
    EtcDicBiogeoregFactory,
    EtcDataHabitattypeRegionFactory,
    EtcDataHabitattypeAutomaticAssessmentFactory,
    HabitattypesManualAssessmentsFactory,
    EtcDicHdHabitat, EtcDicMethodFactory)


@pytest.fixture(autouse=True)
def setup(app):
    EtcDataSpeciesRegionFactory(
        group='Mammals',
        assesment_speciesname='Capra ibex',
        speciesname='Capra ibex',
        range_surface_area=12530)
    SpeciesManualAssessmentFactory(
        assesment_speciesname='Capra ibex',
        range_surface_area=19850,
        region='ALP',
        method_range='2GD',
        decision='OK')
    EtcDataSpeciesAutomaticAssessmentFactory(
        assesment_speciesname='Capra ibex',
        assessment_method='1',
        range_surface_area=19850,
        region='ALP',
    )
    EtcDicBiogeoregFactory()
    EtcDataHabitattypeRegionFactory(
        range_surface_area=1283,
        habitatcode=1110)
    EtcDataHabitattypeAutomaticAssessmentFactory(
        range_surface_area=1283,
        assessment_method='1',
        habitatcode=1110,
        region='ALP',
    )
    HabitattypesManualAssessmentsFactory(
        range_surface_area=1283,
        habitatcode=1110,
        method_range='2XA',
        conclusion_range='FV',
        decision='OK',
        region='ALP',
    )
    EtcDicHdHabitat()
    EtcDicMethodFactory()
    db.session.commit()


@pytest.mark.parametrize("request_args,search_dict", [
    (['/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Capra ibex',
        'region': ''}], {1: '12530', 3: '19850', 5: '19850'}),
    (['/habitat/summary/', {
        'group': 'coastal habitats', 'period': '1', 'subject': '1110',
        'region': ''}], {1: '1283', 3: '1283', 5: '1283'}),
])
def test_summary_range_value(app, client, request_args, search_dict):
    resp = client.get(*request_args)
    for tbody_order_nr, search_text in search_dict.iteritems():
        content_tbody = resp.html.find_all('tbody')[tbody_order_nr]
        range_area_td = content_tbody.find_all('td', {'class': 'number'})[0]
        assert search_text in range_area_td.text


@pytest.mark.parametrize("request_args,search_text", [
    (['/species/progress/', {
        'group': 'Mammals', 'period': '1',  'conclusion': 'range'}],
     '2GD'),
    (['/habitat/progress/', {
        'group': 'coastal habitats', 'period': '1',  'conclusion': 'range'}],
     '2XA')
])
def test_progress_range_value(app, client, request_args, search_text):
    resp = client.get(*request_args)
    assert search_text in resp.html.find('a', {'class': 'conclusion'}).text
