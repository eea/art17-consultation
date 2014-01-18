from pytest import fixture

from art17.models import db
from .factories import (
    DatasetFactory,
)


@fixture(autouse=True)
def setup(app):
    DatasetFactory()
    db.session.commit()


def test_filter_groups_view(app, client):
    pass


def test_filter_species_view(app, client):
    pass


def test_filter_regions_view(app, client):
    pass
