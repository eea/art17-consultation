import pytest

from art17.models import db
from .factories import (
    DatasetFactory,
)


@pytest.fixture(autouse=True)
def setup(app):
    DatasetFactory()
    db.session.commit()


def test_homepage(client, app, set_auth):
    resp = client.get("/")
    assert resp.status_code == 200


@pytest.mark.parametrize(
    "path,args_dict,search_text,elem_found",
    [
        (
            "/species/summary/",
            {"group": "Mammals", "period": "5", "subject": "Canis lupus", "region": ""},
            "Canis lupus",
            True,
        ),
        (
            "/species/summary/",
            {"group": "Mammals", "period": "5", "subject": "Capra ibex", "region": ""},
            "Canis lupus",
            False,
        ),
        (
            "/species/progress/",
            {"period": "5", "group": "Mammals", "conclusion": "population"},
            "Mammals, population",
            True,
        ),
        (
            "/species/progress/",
            {"period": "5", "group": "Fish", "conclusion": "range"},
            "Mammals, population",
            False,
        ),
        (
            "/species/report/",
            {"period": "5", "group": "Mammals", "country": "IT", "region": ""},
            "Mammals, IT",
            True,
        ),
        (
            "/species/report/",
            {"period": "5", "group": "Fish", "country": "EL", "region": ""},
            "Mammals, IT",
            False,
        ),
        (
            "/habitat/summary/",
            {"period": "5", "group": "forests", "subject": "9010", "region": ""},
            "forests, 9010",
            True,
        ),
        (
            "/habitat/summary/",
            {"period": "5", "group": "grasslands", "subject": "6110", "region": ""},
            "forests, 9010",
            False,
        ),
        (
            "/habitat/progress/",
            {"period": 5, "group": "Forests", "conclusion": "range"},
            "Forests, range",
            True,
        ),
        (
            "/habitat/progress/",
            {"period": 5, "group": "Grasslands", "conclusion": "area"},
            "Forests, range",
            False,
        ),
        (
            "/habitat/report/",
            {"period": "5", "group": "Forests", "country": "IT", "region": ""},
            "Forests, IT",
            True,
        ),
        (
            "/habitat/report/",
            {"period": "5", "group": "Grasslands", "country": "EL", "region": ""},
            "Forests, IT",
            False,
        ),
    ],
)
def test_view(client, app, set_auth, path, args_dict, search_text, elem_found):
    resp = client.get(path, args_dict)
    assert resp.status_code == 200
    assert resp.content_type == "text/html"
    assert (search_text in resp.text) == elem_found
