from flask import url_for
from pytest import fixture

from art17.models import db
from .factories import (
    DatasetFactory,
    EtcDataSpeciesRegionFactory,
    EtcDicBiogeoregFactory,
)


@fixture(autouse=True)
def setup(app):
    DatasetFactory()
    EtcDicBiogeoregFactory()
    EtcDataSpeciesRegionFactory(group='reptiles',
                                assesment_speciesname='kitaibelii')
    db.session.commit()


def test_filter_groups_view(app, client):
    url = url_for('common.species-groups', period='5')
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == '-'
    assert resp.json['reptiles'] == 'reptiles'


def test_filter_species_view(app, client):
    url = url_for('summary.species-summary-species', period='5',
                  group='reptiles')
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == '-'
    assert resp.json['kitaibelii'] == 'kitaibelii'


def test_filter_regions_view(app, client):
    url = url_for('summary.species-summary-regions', period='5',
                  subject='kitaibelii')
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == 'All bioregions'
    assert resp.json['ALP'] == 'Alpine'
