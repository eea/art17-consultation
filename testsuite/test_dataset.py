import pytest

from art17 import models

from .conftest import get_request_params
from .factories import (
    CommentFactory,
    DatasetFactory,
    EtcDataHabitattypeAutomaticAssessmentFactory,
    EtcDataSpeciesAutomaticAssessmentFactory,
    EtcDicHdHabitat,
    EtcDicMethodFactory,
    HabitatCommentFactory,
    HabitattypesManualAssessmentsFactory,
    SpeciesManualAssessmentFactory,
)

CANIS_LUPUS = "Canis lupus"
HABCODE = 110


@pytest.fixture
def dataset_app(app):
    DatasetFactory(id=1, name="2001-2006", schema="2006")
    DatasetFactory(id=2, name="2007-2012", schema="2012")
    EtcDicMethodFactory(dataset_id=1, method="1")
    EtcDicMethodFactory(dataset_id=2, method="1")
    # Species
    EtcDataSpeciesAutomaticAssessmentFactory(
        dataset_id=1,
        assessment_method="1",
        percentage_range_surface_area=10,
        percentage_population_mean_size=30,
        percentage_future=50,
        percentage_habitat_surface_area=70,
        percentage_assessment=90,
        assesment_speciesname=CANIS_LUPUS,
        region="ALP",
    )
    EtcDataSpeciesAutomaticAssessmentFactory(
        dataset_id=2,
        assessment_method="1",
        percentage_range_surface_area=20,
        percentage_population_mean_size=40,
        percentage_future=60,
        percentage_habitat_surface_area=80,
        percentage_assessment=100,
        assesment_speciesname=CANIS_LUPUS,
        region="ALP",
    )
    SpeciesManualAssessmentFactory(
        dataset_id=1,
        assesment_speciesname=CANIS_LUPUS,
        region="ALP",
        decision="OK",
        method_range="1",
        method_population="1",
        method_future="1",
        method_habitat="1",
        method_assessment="1",
    )
    SpeciesManualAssessmentFactory(
        dataset_id=2,
        assesment_speciesname=CANIS_LUPUS,
        region="ALP",
        decision="OK",
        method_range="1",
        method_population="1",
        method_future="1",
        method_habitat="1",
        method_assessment="1",
    )
    # Habitats
    EtcDataHabitattypeAutomaticAssessmentFactory(
        dataset_id=1,
        assessment_method="1",
        percentage_range_surface_area=1010,
        percentage_coverage_surface_area=1030,
        percentage_structure=1050,
        percentage_future=1070,
        percentage_assessment=1090,
        habitatcode=110,
        region="ALP",
    )
    EtcDataHabitattypeAutomaticAssessmentFactory(
        dataset_id=2,
        assessment_method="1",
        percentage_range_surface_area=1020,
        percentage_coverage_surface_area=1040,
        percentage_structure=1060,
        percentage_future=1080,
        percentage_assessment=1100,
        habitatcode=110,
        region="ALP",
    )
    HabitattypesManualAssessmentsFactory(
        dataset_id=1,
        subject=110,
        region="ALP",
        decision="OK",
        method_range="1",
        method_area="1",
        method_structure="1",
        method_future="1",
        method_assessment="1",
    )
    HabitattypesManualAssessmentsFactory(
        dataset_id=2,
        subject=110,
        region="ALP",
        decision="OK",
        method_range="1",
        method_area="1",
        method_structure="1",
        method_future="1",
        method_assessment="1",
    )
    models.db.session.commit()


@pytest.mark.parametrize(
    "url, params, expected",
    [
        # Species
        #  get_range_conclusion_value
        (
            "/species/summary/",
            {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 10"',
        ),
        (
            "/species/summary/",
            {"period": 2, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 20"',
        ),
        # get_population_conclusion_value
        (
            "/species/summary/",
            {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 30"',
        ),
        (
            "/species/summary/",
            {"period": 2, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 40"',
        ),
        # get_future_conclusion_value
        (
            "/species/summary/",
            {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 50"',
        ),
        (
            "/species/summary/",
            {"period": 2, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 60"',
        ),
        # get_habitat_conclusion_value
        (
            "/species/summary/",
            {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 70"',
        ),
        (
            "/species/summary/",
            {"period": 2, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 80"',
        ),
        # get_asssesm_conclusion_value
        (
            "/species/summary/",
            {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 90"',
        ),
        (
            "/species/summary/",
            {"period": 2, "subject": CANIS_LUPUS, "region": "ALP"},
            'title=": 100"',
        ),
        # Habitats
        # get_range_conclusion_value
        (
            "/habitat/summary/",
            {"period": 1, "subject": 110, "region": "ALP"},
            'title=": 1010"',
        ),
        (
            "/habitat/summary/",
            {"period": 2, "subject": 110, "region": "ALP"},
            'title=": 1020"',
        ),
        # get_coverage_conclusion_value
        (
            "/habitat/summary/",
            {"period": 1, "subject": 110, "region": "ALP"},
            'title=": 1030"',
        ),
        (
            "/habitat/summary/",
            {"period": 2, "subject": 110, "region": "ALP"},
            'title=": 1040"',
        ),
        # percentage_structure
        (
            "/habitat/summary/",
            {"period": 1, "subject": 110, "region": "ALP"},
            'title=": 1050"',
        ),
        (
            "/habitat/summary/",
            {"period": 2, "subject": 110, "region": "ALP"},
            'title=": 1060"',
        ),
        # percentage_future
        (
            "/habitat/summary/",
            {"period": 1, "subject": 110, "region": "ALP"},
            'title=": 1070"',
        ),
        (
            "/habitat/summary/",
            {"period": 2, "subject": 110, "region": "ALP"},
            'title=": 1080"',
        ),
        # assessment
        (
            "/habitat/summary/",
            {"period": 1, "subject": 110, "region": "ALP"},
            'title=": 1090"',
        ),
        (
            "/habitat/summary/",
            {"period": 2, "subject": 110, "region": "ALP"},
            'title=": 1100"',
        ),
    ],
)
def test_species_conclusion_values(
    client, set_auth, dataset_app, url, params, expected
):
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert expected in result.body.decode()


def test_get_subject_details(client, set_auth, dataset_app):
    EtcDicHdHabitat(dataset_id=1, habcode=HABCODE, name="foo foo")
    EtcDicHdHabitat(dataset_id=2, habcode=HABCODE, name="boo boo")
    models.db.session.commit()

    url = "/habitat/summary/"
    params = {"period": 1, "subject": HABCODE, "region": ""}

    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "foo foo" in result.body.decode()

    params["period"] = 2
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "boo boo" in result.body.decode()


def test_unread_comments_species(client, set_auth, dataset_app):
    CommentFactory(id=1, dataset_id=1, region="ALP", assesment_speciesname=CANIS_LUPUS)
    models.db.session.commit()

    url = "/species/summary/"
    params = {"period": 1, "subject": CANIS_LUPUS, "region": "ALP"}

    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result

    params["period"] = 2
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/0" in result

    CommentFactory(id=2, dataset_id=2, region="ALP", assesment_speciesname=CANIS_LUPUS)
    models.db.session.commit()

    params["period"] = 1
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result

    params["period"] = 2

    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result


def test_unread_comments_habitat(client, set_auth, dataset_app):
    HabitatCommentFactory(id=1, dataset_id=1, region="ALP", habitat=HABCODE)
    models.db.session.commit()

    url = "/habitat/summary/"
    params = {"period": 1, "subject": HABCODE, "region": "ALP"}

    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result

    params["period"] = 2
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/0" in result

    HabitatCommentFactory(id=2, dataset_id=2, region="ALP", habitat=HABCODE)
    models.db.session.commit()

    params["period"] = 1
    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result

    params["period"] = 2

    result = client.get(*get_request_params("get", [url, params]))
    assert result.status_code == 200
    assert "0/1" in result
