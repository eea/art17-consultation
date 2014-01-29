import pytest

from art17.models import db
from .factories import (
    EtcDataSpeciesRegionFactory,
    SpeciesManualAssessmentFactory,
    EtcDataSpeciesAutomaticAssessmentFactory,
    EtcDicBiogeoregFactory,
    EtcDataHabitattypeRegionFactory,
    EtcDataHabitattypeAutomaticAssessmentFactory,
    HabitattypesManualAssessmentsFactory)


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
        range_surface_area=19850)
    EtcDicBiogeoregFactory()
    EtcDataHabitattypeRegionFactory(
        range_surface_area=1283,
        habitatcode=1110)
    EtcDataHabitattypeAutomaticAssessmentFactory(
        range_surface_area=1283,
        habitatcode=1110)
    HabitattypesManualAssessmentsFactory(
        range_surface_area=1283,
        habitatcode=1110)
    db.session.commit()


@pytest.mark.parametrize("request_args,tbody_order_nr,search_text", [
    (['/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Capra ibex',
        'region': ''}], 1, '12530'),
    (['/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Capra ibex',
        'region': ''}], 3, '19850'),
    (['/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Capra ibex',
        'region': ''}], 5, '19850'),
    (['/habitat/summary/', {
        'group': 'coastal habitats', 'period': '1', 'subject': '1110',
        'region': ''}], 1, '1283'),
    (['/habitat/summary/', {
        'group': 'coastal habitats', 'period': '1', 'subject': '1110',
        'region': ''}], 3, '1283'),
    (['/habitat/summary/', {
        'group': 'coastal habitats', 'period': '1', 'subject': '1110',
        'region': ''}], 5, '1283'),
])
def test_summary_range_value(app, client, request_args, tbody_order_nr,
                             search_text):
    resp = client.get(*request_args)
    content_tbody = resp.html.find_all('tbody')[tbody_order_nr]
    range_area_td = content_tbody.find_all('td', {'class': 'number'})[0]
    assert search_text in range_area_td.text


def test_species_progress_range_value(app, client):
    resp = client.get('/species/progress/', {
        'group': 'Mammals', 'period': '1',  'conclusion': 'range'})
    assert '2GD' in resp.html.find('td').text
