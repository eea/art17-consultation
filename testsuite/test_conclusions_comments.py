import pytest

from art17 import models

from .conftest import create_user, force_login, get_request_params
from .factories import (
    CommentFactory,
    DatasetFactory,
    HabitatCommentFactory,
    HabitattypesManualAssessmentsFactory,
    SpeciesManualAssessmentFactory,
)


@pytest.fixture
def setup(app):
    SpeciesManualAssessmentFactory()
    CommentFactory()
    HabitattypesManualAssessmentsFactory()
    HabitatCommentFactory()
    models.db.session.commit()


@pytest.mark.parametrize(
    "request_type, request_args, post_params, user, expect_errors, "
    "status_code, assert_condition",
    # Species
    # Anonymous user
    [
        (
            "post",
            ["/species/comments/5/Canis lupus/BOR/someuser/", {"MS": "EU27"}],
            {"comment": "I cannot post comments"},
            [],
            True,
            403,
            "",
        ),
        (
            "post",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I cannot edit this comment"},
            [],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            [],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            [],
            True,
            403,
            "",
        ),
        # User that posted a comment already
        (
            "post",
            ["/species/comments/5/Canis lupus/BOR/someuser/", {"MS": "EU27"}],
            {"comment": "I cannot post comments"},
            ["testuser"],
            True,
            403,
            "",
        ),
        (
            "post",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I can edit this comment!"},
            ["testuser"],
            False,
            302,
            "'I can edit this comment!' in resp.html.text",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            ["testuser"],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["testuser"],
            False,
            200,
            "'Undelete' in resp.html.text",
        ),
        # User that didn't post any comments
        (
            "post",
            ["/species/comments/5/Canis lupus/BOR/someuser/", {"MS": "EU27"}],
            {"comment": "I can post comments!"},
            ["newuser"],
            False,
            302,
            "'I can post comments!' in resp.html.text",
        ),
        (
            "post",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I can't edit testuser's comment"},
            ["newuser"],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            ["newuser"],
            False,
            200,
            "'Mark as unread' in resp.html.text",
        ),
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["newuser"],
            True,
            403,
            "",
        ),
        # User with admin role
        (
            "get",
            [
                "/species/comments/5/Canis lupus/BOR/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["adminuser", ["admin"]],
            False,
            200,
            "'Undelete' in resp.html.text",
        ),
        # Habitat
        # Anonymous user
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {
                    "MS": "EU27",
                },
            ],
            {"comment": "I cannot post comments"},
            [],
            True,
            403,
            "",
        ),
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I cannot edit this comment"},
            [],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            [],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            [],
            True,
            403,
            "",
        ),
        # User that posted a comment already
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {
                    "MS": "EU27",
                },
            ],
            {"comment": "I cannot post comments"},
            ["testuser"],
            True,
            403,
            "",
        ),
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I can edit this comment!"},
            ["testuser"],
            False,
            302,
            "'I can edit this comment!' in resp.html.text",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            ["testuser"],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["testuser"],
            False,
            200,
            "'Undelete' in resp.html.text",
        ),
        # User that didn't post any comments
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {
                    "MS": "EU27",
                },
            ],
            {"comment": "I can post comments!"},
            ["newuser"],
            False,
            302,
            "'I can post comments!' in resp.html.text",
        ),
        (
            "post",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "edit": 1},
            ],
            {"comment": "I can't edit testuser's comment"},
            ["newuser"],
            True,
            403,
            "",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "toggle": 1, "read": False},
            ],
            {},
            ["newuser"],
            False,
            200,
            "'Mark as unread' in resp.html.text",
        ),
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["newuser"],
            True,
            403,
            "",
        ),
        # User with admin role
        (
            "get",
            [
                "/habitat/comments/5/1110/MATL/someuser/",
                {"MS": "EU27", "delete": 1, "deleted": 0},
            ],
            {},
            ["adminuser", ["admin"]],
            False,
            200,
            "'Undelete' in resp.html.text",
        ),
    ],
)
def test_comments(
    app,
    client,
    setup,
    set_auth,
    request_type,
    request_args,
    post_params,
    user,
    expect_errors,
    status_code,
    assert_condition,
):
    user_obj = create_user("testuser")
    if user:
        if user[0] != "testuser":
            if len(user) > 1:
                roles = user[1]
            else:
                roles = []
            user_obj = create_user(user[0], roles)
        force_login(client, user_obj.fs_uniquifier)

    resp = getattr(client, request_type)(
        *get_request_params(request_type, request_args, post_params),
        expect_errors=expect_errors
    )
    assert resp.status_code == status_code

    if resp.status_code == 302:
        resp = resp.follow()

    if assert_condition:
        assert eval(assert_condition)


@pytest.mark.parametrize(
    "manual_assessment_cls",
    [
        (SpeciesManualAssessmentFactory),
        (HabitattypesManualAssessmentsFactory),
    ],
)
def test_count_read_comments_no_comments(app, manual_assessment_cls):
    record = manual_assessment_cls()
    assert record.comments_count_read("someuser") == 0


@pytest.mark.parametrize(
    "manual_assessment_cls, comment_cls, deleted, expected_result",
    [
        (SpeciesManualAssessmentFactory, CommentFactory, 0, 1),
        (SpeciesManualAssessmentFactory, CommentFactory, 1, 0),
        (HabitattypesManualAssessmentsFactory, HabitatCommentFactory, 0, 1),
        (HabitattypesManualAssessmentsFactory, HabitatCommentFactory, 1, 0),
    ],
)
def test_count_read_comments_deleted(
    app, manual_assessment_cls, comment_cls, deleted, expected_result
):
    record = manual_assessment_cls()
    comment = comment_cls(deleted=deleted)
    models.db.session.commit()

    user = create_user("someuser")
    comment.readers.append(user)
    models.db.session.commit()
    assert record.comments_count_read("someuser") == expected_result


@pytest.mark.parametrize(
    "manual_assessment_cls, comment_cls, request_args",
    [
        (
            SpeciesManualAssessmentFactory,
            CommentFactory,
            [
                "/species/summary/",
                {
                    "period": 5,
                    "group": "Mammals",
                    "subject": "Canis lupus",
                    "region": "ALP",
                },
            ],
        ),
        (
            HabitattypesManualAssessmentsFactory,
            HabitatCommentFactory,
            [
                "/habitat/summary/",
                {
                    "period": 5,
                    "group": "coastal habitats",
                    "subject": 1110,
                    "region": "ALP",
                },
            ],
        ),
    ],
)
def test_count_read_comments_view(
    app, client, set_auth, manual_assessment_cls, comment_cls, request_args
):
    DatasetFactory()
    manual_assessment_cls(region="ALP")
    comment = comment_cls(region="ALP")
    models.db.session.commit()

    user = create_user(
        "someuser",
        [
            "etc",
        ],
    )
    comment.readers.append(user)
    models.db.session.commit()

    force_login(client, user.fs_uniquifier)
    resp = client.get(*get_request_params("get", request_args))

    assert resp.status_code == 200
    assert resp.html.find("a", {"title": "Comments: Read/Total"}).text.strip() == "1/1"
