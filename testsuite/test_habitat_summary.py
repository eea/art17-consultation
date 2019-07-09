import pytest

from flask import url_for
from pytest import fixture

from art17.models import db
from .factories import (
    DatasetFactory,
    EtcDicHdHabitat,
    EtcDicBiogeoregFactory,
    EtcDataHabitattypeRegionFactory,
)


@fixture(autouse=True)
def setup(app):
    DatasetFactory()
    EtcDicHdHabitat()
    EtcDicBiogeoregFactory()
    EtcDataHabitattypeRegionFactory()
    db.session.commit()


def test_filter_groups_view(app, client):
    url = url_for('common.habitat-groups', period='1')
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == '-'
    assert resp.json['Coastal habitats'] == 'Coastal habitats'


def test_filter_species_view(app, client):
    url = url_for('summary.habitat-summary-species', period='1',
                  group='coastal habitats')
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == '-'
    assert resp.json['1110'].startswith('1110 Sandbanks')


def test_filter_regions_view(app, client):
    url = url_for('summary.habitat-summary-regions', period='1',
                  subject='1110')
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == 'All bioregions'
    print resp.json
    assert resp.json['ALP'] == 'Alpine'
