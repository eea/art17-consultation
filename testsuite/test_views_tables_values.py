import pytest

from art17.models import db
from . import factories


@pytest.fixture(autouse=True)
def setup(app):
    factories.DatasetFactory(id=5, schema='2018', name='2013-2018',
                             habitat_map_url='', species_map_url='')
    factories.EtcDataSpeciesRegionFactory(
        group='Mammals',
        dataset_id=5,
        assesment_speciesname='Capra ibex',
        speciesname='Capra ibex',
        range_surface_area=12530)
    factories.SpeciesManualAssessmentFactory(
        assesment_speciesname='Capra ibex',
        range_surface_area=19850,
        dataset_id=5,
        region='ALP',
        method_range='2GD',
        conclusion_range='U1',
        decision='OK')
    factories.EtcDataSpeciesAutomaticAssessmentFactory(
        assesment_speciesname='Capra ibex',
        dataset_id=5,
        assessment_method='1',
        range_surface_area=19850,
        region='ALP',
    )
    factories.EtcDicBiogeoregFactory()
    factories.EtcDataHabitattypeRegionFactory(
        range_surface_area=1283,
        dataset_id=5,
        habitatcode=1110)
    factories.EtcDataHabitattypeAutomaticAssessmentFactory(
        range_surface_area=1283,
        assessment_method='1',
        dataset_id=5,
        habitatcode=1110,
        region='ALP',
    )
    factories.HabitattypesManualAssessmentsFactory(
        range_surface_area=1283,
        habitatcode=1110,
        dataset_id=5,
        method_range='2XA',
        conclusion_range='FV',
        decision='OK',
        region='ALP',
    )
    factories.EtcDicHdHabitat()
    factories.EtcDicMethodFactory()
    db.session.commit()


@pytest.mark.parametrize("request_args,search_dict", [
    (['/species/summary/', {
        'group': 'Mammals', 'period': '5', 'subject': 'Capra ibex',
        'region': ''}], {1: '12530', 3: '19850', 5: '19850'}),
    (['/habitat/summary/', {
        'group': 'coastal habitats', 'period': '5', 'subject': '1110',
        'region': ''}], {1: '1283', 3: '1283', 5: '1283'}),
])
def test_summary_range_value(client, set_auth, app, request_args, search_dict):
    resp = client.get(*request_args)
    for tbody_order_nr, search_text in search_dict.iteritems():
        content_tbody = resp.html.find_all('tbody')[tbody_order_nr]
        range_area_td = content_tbody.find_all('td', {'class': 'number'})[0]
        assert search_text in range_area_td.text


@pytest.mark.parametrize("request_args,search_text", [
    (['/species/progress/', {
        'group': 'Mammals', 'period': '5',  'conclusion': 'range'}],
     'U1'),
    (['/habitat/progress/', {
        'group': 'coastal habitats', 'period': '5',  'conclusion': 'range'}],
     'FV')
])
def test_progress_range_value(client, set_auth, app, request_args, search_text):
    resp = client.get(*request_args)
    assert search_text in resp.html.find('a', {'class': 'conclusion'}).text
