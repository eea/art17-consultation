import pytest
from werkzeug.datastructures import MultiDict

from art17.forms import (
    EMPTY_FORM,
    METH_CONCL_MANDATORY,
    METH_CONCL_PAIR_MANDATORY,
    NOT_NUMERIC_VALUES,
    SummaryManualFormSpecies,
)
from art17.models import db

from .factories import DatasetFactory, EtcDicMethodFactory


@pytest.fixture(autouse=True)
def setup(app):
    DatasetFactory()
    EtcDicMethodFactory()
    db.session.commit()


@pytest.mark.parametrize(
    "data,error,field",
    [
        ({}, EMPTY_FORM, "form_errors"),
        ({"range_surface_area": "10"}, METH_CONCL_MANDATORY, "form_errors"),
        (
            {"range_surface_area": "11", "method_range": "1"},
            METH_CONCL_PAIR_MANDATORY,
            "conclusion_range",
        ),
        (
            {"range_surface_area": "asdfasdpl;"},
            NOT_NUMERIC_VALUES,
            "range_surface_area",
        ),
    ],
)
def test_basic_errors(app, data, error, field):
    form = SummaryManualFormSpecies(MultiDict(data))
    form.setup_choices(dataset_id=5)
    form.validate()

    field = getattr(form, field)
    assert error in field.errors
