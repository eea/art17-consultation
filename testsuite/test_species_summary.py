from flask import url_for
from pytest import fixture

from art17.models import db, Dataset

from .factories import (
    EtcDataSpeciesRegionFactory,
    EtcDicBiogeoregFactory,
)


@fixture(autouse=True)
def setup(app):
    EtcDicBiogeoregFactory()
    EtcDataSpeciesRegionFactory(group="reptiles", assessment_speciesname="kitaibelii")
    db.session.commit()


def test_filter_groups_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for("common.species-groups", period=dataset_2024.id)
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "-"
    assert resp.json[1][1] == "reptiles"


def test_filter_species_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for(
        "summary.species-summary-species", period=dataset_2024.id, group="reptiles"
    )
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "-"
    assert resp.json[1][1] == "kitaibelii"


def test_filter_regions_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for(
        "summary.species-summary-regions", period=dataset_2024.id, subject="kitaibelii"
    )
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "All bioregions"
    assert resp.json[1][1] == "Alpine"
