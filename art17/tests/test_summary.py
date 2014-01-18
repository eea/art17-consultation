from flask import url_for
from pytest import fixture

from art17.models import db
from .factories import (
    DatasetFactory,
    EtcDataSpeciesRegionFactory
)


@fixture(autouse=True)
def setup(app):
    DatasetFactory()
    EtcDataSpeciesRegionFactory(group='reptiles')
    db.session.commit()


def test_filter_groups_view(app, client):
    url = url_for('summary.species-summary-groups', period='1')
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == 'application/json'
    assert resp.json[''] == '-'
    assert resp.json['reptiles'] == 'reptiles'

