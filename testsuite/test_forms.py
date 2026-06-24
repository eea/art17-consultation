import pytest
from werkzeug.datastructures import MultiDict

from art17.forms import (
    EMPTY_FORM,
    METH_CONCL_MANDATORY,
    NOT_NUMERIC_VALUES,
    SummaryManualFormSpecies,
)
from art17.models import db, Dataset

from .factories import EtcDicMethodFactory


@pytest.fixture(autouse=True)
def setup(app):
    EtcDicMethodFactory()
    db.session.commit()


@pytest.mark.parametrize(
    "data,error,field_name",
    [
        ({}, EMPTY_FORM, "form_errors"),
        ({"range_surface_area": "10"}, METH_CONCL_MANDATORY, "form_errors"),
        (
            {"range_surface_area": "asdfasdpl;"},
            NOT_NUMERIC_VALUES,
            "range_surface_area",
        ),
    ],
)
def test_basic_errors(app, data, error, field_name):
    form = SummaryManualFormSpecies(MultiDict(data))
    dataset_2018 = Dataset.query.filter_by(schema="2018").first()
    form.setup_choices(dataset_id=dataset_2018.id)
    form.validate()

    field = getattr(form, field_name)
    if field_name == "form_errors":
        assert error in field
    else:
        assert error in field.errors
