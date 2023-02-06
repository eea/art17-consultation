from flask import url_for
from pytest import fixture

from art17.models import db

from .factories import (DatasetFactory, EtcDataHabitattypeRegionFactory,
                        EtcDicBiogeoregFactory, EtcDicHdHabitat)


@fixture(autouse=True)
def setup(app):
    DatasetFactory()
    EtcDicHdHabitat()
    EtcDicBiogeoregFactory()
    EtcDataHabitattypeRegionFactory()
    db.session.commit()


def test_filter_groups_view(app, client):
    url = url_for("common.habitat-groups", period="5")
    resp = client.get(url)

    assert resp.status_code == 200
    assert resp.content_type == "application/json"

    assert resp.json[0][1] == "-"
    assert resp.json[1][1] == "Coastal habitats"


def test_filter_species_view(app, client):
    url = url_for(
        "summary.habitat-summary-species", period="5", group="coastal habitats"
    )
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "-"
    assert resp.json[1][1].startswith("1110 Sandbanks")


def test_filter_regions_view(app, client):
    url = url_for("summary.habitat-summary-regions", period="5", subject="1110")
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == "application/json"
    assert resp.json[0][1] == "All bioregions"
    print(resp.json)
    assert resp.json[1][1] == "Alpine"
