from flask import url_for
from pytest import fixture

from art17.models import db, Dataset

from .factories import (
    EtcDataHabitattypeRegionFactory,
    EtcDicBiogeoregFactory,
    EtcDicHdHabitat,
)


@fixture(autouse=True)
def setup(app):
    EtcDicHdHabitat()
    EtcDicBiogeoregFactory()
    EtcDataHabitattypeRegionFactory()
    db.session.commit()


def test_filter_groups_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for("common.habitat-groups", period=dataset_2024.id)
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == "application/json"

    assert resp.json[0][1] == "-"
    assert resp.json[1][1] == "Coastal habitats"


def test_filter_species_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for(
        "summary.habitat-summary-species",
        period=dataset_2024.id,
        group="coastal habitats",
    )
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "-"
    assert resp.json[1][1].startswith("1110 Sandbanks")


def test_filter_regions_view(app, client):
    dataset_2024 = Dataset.query.filter_by(schema="2024").first()
    url = url_for(
        "summary.habitat-summary-regions", period=dataset_2024.id, subject="1110"
    )
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "All bioregions"
    print(resp.json)
    assert resp.json[1][1] == "Alpine"
