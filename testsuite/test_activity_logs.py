import pytest

from art17 import models

from .conftest import create_user, force_login
from .factories import (
    CommentFactory,
    HabitatCommentFactory,
    HabitattypesManualAssessmentsFactory,
    SpeciesManualAssessmentFactory,
)


@pytest.fixture
def setup(app):
    SpeciesManualAssessmentFactory(last_update="2014-03-20 18:11")
    CommentFactory(post_date="2014-03-20", author_id="author")
    HabitattypesManualAssessmentsFactory(last_update="2014-03-20 18:11")
    HabitatCommentFactory(post_date="2014-03-20", author_id="author")
    models.db.session.commit()


@pytest.fixture
def setup_deleted(app):
    SpeciesManualAssessmentFactory(deleted=1)
    CommentFactory(deleted=1)
    HabitattypesManualAssessmentsFactory(deleted=1)
    HabitatCommentFactory(deleted=1)
    models.db.session.commit()


@pytest.fixture
def setup_read(app):
    SpeciesManualAssessmentFactory(region="ALP")
    HabitattypesManualAssessmentsFactory(region="ALP")


@pytest.mark.parametrize(
    "user, request_args, expect_errors, status_code",
    [
        (None, "/history/species/", True, 403),
        (None, "/history/habitat/", True, 403),
        ("testuser", "/history/species/", False, 200),
        ("testuser", "/history/habitat/", False, 200),
    ],
)
def test_view(app, client, set_auth, user, request_args, expect_errors, status_code):
    if user:
        user_obj = create_user(user)
        force_login(client, user_obj.fs_uniquifier)
    resp = client.get(request_args, expect_errors=expect_errors)
    assert resp.status_code == status_code


@pytest.mark.parametrize(
    "user, request_args, exp_conclusion_fields, exp_comment_fields",
    [
        (
            "testuser",
            "/history/species/",
            ["Canis lupus", "BOR", "someuser", "2014-03-20 18:11"],
            ["Canis lupus", "BOR", "author", "someuser", "2014-03-20", "False"],
        ),
        (
            "testuser",
            "/history/habitat/",
            ["1110", "MATL", "someuser", "2014-03-20 18:11"],
            ["1110", "MATL", "author", "someuser", "2014-03-20", "False"],
        ),
    ],
)
def test_data(
    app,
    client,
    set_auth,
    setup,
    user,
    request_args,
    exp_conclusion_fields,
    exp_comment_fields,
):
    user_obj = create_user(user)
    force_login(client, user_obj.fs_uniquifier)
    resp = client.get(request_args)
    assert resp.status_code == 200

    comments, conclusions = resp.html.find_all("table")
    comment_fields = [c.text for c in comments.find_all("td")]
    conclusion_fields = [c.text for c in conclusions.find_all("td")]
    assert comment_fields == exp_comment_fields
    assert conclusion_fields == exp_conclusion_fields


@pytest.mark.parametrize(
    "user, request_args",
    [
        ("testuser", "/history/species/"),
        ("testuser", "/history/habitat/"),
    ],
)
def test_deleted(app, client, set_auth, setup_deleted, user, request_args):
    user_obj = create_user(user)
    force_login(client, user_obj.fs_uniquifier)
    resp = client.get(request_args)
    assert resp.status_code == 200
    assert len(resp.html.find_all("td")) == 0


@pytest.mark.parametrize(
    "username, request_args, comment_cls, exp_comment_fields",
    [
        (
            "testuser",
            "/history/species/",
            CommentFactory,
            ["Canis lupus", "ALP", "author", "someuser", "2014-03-20", "True"],
        ),
        (
            "testuser",
            "/history/habitat/",
            HabitatCommentFactory,
            ["1110", "ALP", "author", "someuser", "2014-03-20", "True"],
        ),
    ],
)
def test_read_comments(
    app,
    client,
    set_auth,
    setup_read,
    username,
    request_args,
    comment_cls,
    exp_comment_fields,
):
    user = create_user(username)
    force_login(client, user.fs_uniquifier)

    comment = comment_cls(region="ALP", post_date="2014-03-20", author_id="author")
    models.db.session.commit()

    comment.readers.append(user)
    models.db.session.commit()

    resp = client.get(request_args)
    assert resp.status_code == 200

    comment_fields = [c.text for c in resp.html.find("table").find_all("td")]
    assert comment_fields == exp_comment_fields
