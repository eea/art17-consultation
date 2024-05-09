import pytest

from art17.auth.providers import set_user
from art17.models import RegisteredUser, Wiki, WikiChange, WikiComment, db

from .conftest import create_user, force_login, get_request_params
from .factories import (
    DatasetFactory,
    EtcDicBiogeoregFactory,
    WikiChangeFactory,
    WikiCommentFactory,
    WikiFactory,
    WikiTrailChangeFactory,
    WikiTrailFactory,
)


@pytest.fixture
def setup(app):
    DatasetFactory(id=5, schema="2018", name="2013-2018")
    WikiFactory()
    WikiChangeFactory()
    WikiFactory(id=2, region_code="", habitatcode=1110)
    WikiChangeFactory(
        id=2,
        wiki_id=2,
        body="The conservation status in the marine Baltic region",
    )
    EtcDicBiogeoregFactory(reg_code="CON", reg_name="Continental")
    WikiTrailFactory()
    WikiTrailChangeFactory()
    EtcDicBiogeoregFactory(reg_code="MBAL", reg_name="Marine Baltic")
    WikiTrailFactory(id=2, region_code="MBAL", habitatcode=1110)
    WikiTrailChangeFactory(
        id=2, wiki_id=2, body="Method 1 was used to evaluate the subconclusion"
    )
    WikiCommentFactory()
    WikiCommentFactory(id=2, author_id="otheruser")
    WikiChangeFactory(id=3, wiki_id=1, body="New revision.", active=0)
    db.session.commit()


def get_instance(models_cls, **kwargs):
    return models_cls.query.filter_by(**kwargs).first()


@pytest.mark.parametrize(
    "request_args",
    [
        (
            [
                "/species/summary/datasheet/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ]
        ),
        (
            [
                "/species/summary/audittrail/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ]
        ),
        (
            [
                "/habitat/summary/datasheet/",
                {"period": "5", "subject": "9010", "region": ""},
            ]
        ),
        (
            [
                "/habitat/summary/audittrail/",
                {"period": "5", "subject": "9010", "region": ""},
            ]
        ),
    ],
)
def test_empty_view(app, client, request_args):
    resp = client.get(*request_args)
    assert resp.status_code == 200
    assert resp.content_type == "text/html"
    assert resp.html.find(id="active-wiki").text.strip() == ""


@pytest.mark.parametrize(
    "request_args, search_text",
    [
        (
            [
                "/species/summary/datasheet/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            "The wolf was the world's most widely distributed mammal.",
        ),
        (
            [
                "/species/summary/audittrail/",
                {"period": "5", "subject": "Canis lupus", "region": "CON"},
            ],
            "For Poland: present range, population and habitat",
        ),
        (
            [
                "/habitat/summary/datasheet/",
                {"period": "5", "subject": "1110", "region": ""},
            ],
            "The conservation status in the marine Baltic region",
        ),
        (
            [
                "/habitat/summary/audittrail/",
                {"period": "5", "subject": "1110", "region": "MBAL"},
            ],
            "Method 1 was used to evaluate the subconclusion",
        ),
    ],
)
def test_non_auth_view(app, setup, client, request_args, search_text):
    create_user("testuser", app)
    create_user("otheruser", app)
    resp = client.get(*request_args)
    assert resp.status_code == 200
    assert resp.content_type == "text/html"
    assert resp.html.find(id="active-wiki").text.strip() == search_text


@pytest.mark.parametrize(
    "request_type, request_args, post_params",
    [
        (
            "post",
            [
                "/species/summary/datasheet/page_history/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"revision_id": 1},
        ),
        (
            "post",
            [
                "/species/summary/datasheet/add_comment/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"text": "Test add comment."},
        ),
        (
            "post",
            [
                "/species/summary/datasheet/edit_page/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"text": "Test edit page."},
        ),
        (
            "post",
            [
                "/species/summary/datasheet/edit_comment/",
                {
                    "period": "5",
                    "subject": "Canis lupus",
                    "region": "",
                    "comment_id": 1,
                },
            ],
            {"text": "Test edit comment."},
        ),
        (
            "get",
            [
                "/species/summary/datasheet/manage_comment/",
                {"comment_id": 1, "toggle": "read", "period": "5"},
            ],
            {},
        ),
        (
            "get",
            ["/species/summary/datasheet/get_revision/", {"revision_id": 1}],
            {},
        ),
    ],
)
def test_perms(app, setup, set_auth, client, request_type, request_args, post_params):
    resp = getattr(client, request_type)(
        *get_request_params(request_type, request_args, post_params), expect_errors=True
    )
    assert resp.status_code == 403


@pytest.mark.parametrize(
    "request_type, request_args, post_params",
    [
        # Test (un-)deleting someone else's comment
        (
            "get",
            [
                "/species/summary/datasheet/manage_comment/",
                {"comment_id": 1, "toggle": "del", "period": "5"},
            ],
            {},
        ),
        # Test marking as (un-)read current user's comment
        (
            "get",
            [
                "/species/summary/datasheet/manage_comment/",
                {"comment_id": 2, "toggle": "read", "period": "5"},
            ],
            {},
        ),
        # Test editing someone else's comment
        (
            "post",
            [
                "/species/summary/datasheet/edit_comment/",
                {
                    "period": "5",
                    "subject": "Canis lupus",
                    "region": "",
                    "comment_id": 1,
                },
            ],
            {"text": "Test edit comment."},
        ),
        # Test adding more a second comment
        (
            "post",
            [
                "/species/summary/datasheet/add_comment/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"text": "Test add comment."},
        ),
        # Getting revision info, unavailable to public
        (
            "get",
            ["/species/summary/datasheet/get_revision/", {"revision_id": 999}],
            {},
        ),
    ],
)
def test_perms_auth_user(
    app, setup, set_auth, client, request_type, request_args, post_params
):
    create_user("otheruser", app)
    set_user("otheruser", app)
    resp = getattr(client, request_type)(
        *get_request_params(request_type, request_args, post_params), expect_errors=True
    )
    assert resp.status_code == 403


@pytest.mark.parametrize(
    "request_type, request_args, post_params",
    [
        (
            "post",
            [
                "/species/summary/datasheet/page_history/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"revision_id": 999},
        ),
        (
            "post",
            [
                "/species/summary/datasheet/edit_comment/",
                {
                    "period": "5",
                    "subject": "Canis lupus",
                    "region": "",
                    "comment_id": 999,
                },
            ],
            {"text": "Test edit comment."},
        ),
        # ('get', ['/species/summary/datasheet/manage_comment/', {
        #     'comment_id': 999, 'toggle': 'read', 'period': '5'}], {}),
    ],
)
def test_404_error(
    app, setup, set_auth, client, request_type, request_args, post_params
):
    otheruser = create_user("otheruser", app)
    set_user("otheruser", app)
    force_login(client, otheruser.fs_uniquifier)
    resp = getattr(client, request_type)(
        *get_request_params(request_type, request_args, post_params), expect_errors=True
    )
    assert resp.status_code == 404


@pytest.mark.xfail
def test_change_active_revision(
    app, setup, set_auth, client
):  # can't modify when dataset is readonly
    otheruser = create_user("otheruser", app, role_names=["etc"])
    set_user("otheruser")
    force_login(client, otheruser.fs_uniquifier)
    client.post(
        *get_request_params(
            "post",
            [
                "/species/summary/datasheet/page_history/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"revision_id": 3},
        )
    )
    assert get_instance(WikiChange, id=1).active == 0
    assert get_instance(WikiChange, id=3).active == 1


@pytest.mark.xfail
def test_add_comment(
    app, setup, set_auth, client
):  # can't modify when dataset is readonly
    newuser = create_user("newuser", app)
    set_user("newuser")
    force_login(client, newuser.fs_uniquifier)
    request_data = (
        "post",
        [
            "/species/summary/datasheet/add_comment/",
            {"period": "5", "subject": "Canis lupus", "region": ""},
        ],
        {"comment": "Test add comment."},
    )
    client.post(*get_request_params(*request_data))
    request_args = request_data[1][1]
    wiki = get_instance(
        Wiki,
        dataset_id=request_args["period"],
        assesment_speciesname=request_args["subject"],
        region_code=request_args["region"],
    )
    assert request_data[2]["comment"] in [c.comment for c in wiki.comments]


@pytest.mark.xfail
def test_edit_page(
    app, setup, set_auth, client
):  # can't modify when dataset is readonly
    testuser = create_user("testuser", app, role_names=["etc"])
    set_user("testuser")
    force_login(client, testuser.fs_uniquifier)
    client.post(
        *get_request_params(
            "post",
            [
                "/species/summary/datasheet/edit_page/",
                {"period": "5", "subject": "Canis lupus", "region": ""},
            ],
            {"text": "Test edit page."},
        )
    )
    assert get_instance(WikiChange, id=1).active == 0
    assert get_instance(WikiChange, body="Test edit page.").active == 1


@pytest.mark.xfail
def test_edit_comment(
    app, setup, set_auth, client
):  # can't modify when dataset is readonly
    testuser = create_user("testuser", app, role_names=["stakeholder"])
    set_user("testuser")
    force_login(client, testuser.fs_uniquifier)
    client.post(
        *get_request_params(
            "post",
            [
                "/species/summary/datasheet/edit_comment/",
                {
                    "period": "5",
                    "subject": "Canis lupus",
                    "region": "",
                    "comment_id": 1,
                },
            ],
            {"comment": "Test edit comment."},
        )
    )
    assert get_instance(WikiComment, id=1).comment == "Test edit comment."


@pytest.mark.xfail
def test_toggle_del(app, setup, set_auth, client):
    testuser = create_user("testuser", app)
    set_user("testuser")
    force_login(client, testuser.fs_uniquifier)
    initial_value = get_instance(WikiComment, id=1).deleted or 0
    client.get(
        "/species/summary/datasheet/manage_comment/",
        {"comment_id": 1, "toggle": "del", "period": "5"},
    )
    assert get_instance(WikiComment, id=1).deleted == 1 - initial_value


@pytest.mark.xfail
def test_toggle_read(app, setup, set_auth, client):
    otheruser = create_user("otheruser", app)
    set_user("otheruser")
    force_login(client, otheruser.fs_uniquifier)

    def get_value():
        return (
            get_instance(WikiComment, id=1)
            in get_instance(RegisteredUser, id="otheruser").read_comments
        )

    initial_value = get_value()
    client.get(
        "/species/summary/datasheet/manage_comment/",
        {"comment_id": 1, "toggle": "read", "period": "5"},
    )
    assert get_value() is not initial_value


def test_get_revision(app, setup, set_auth, client):
    testuser = create_user("testuser", app, role_names=["etc"])
    set_user("testuser")
    force_login(client, testuser.fs_uniquifier)

    resp = client.get("/species/summary/datasheet/get_revision/", {"revision_id": 1})
    assert (
        resp.html.text == "The wolf was the world's most widely " "distributed mammal."
    )


@pytest.mark.parametrize("roles", [(["etc"]), (["admin"])])
def test_hide_adm_etc_username(app, setup, set_auth, client, roles):
    create_user("testuser", app, roles, "Secret Name", "Test Insitution")
    otheruser = create_user("otheruser", app)
    set_user("otheruser")
    force_login(client, otheruser.fs_uniquifier)

    resp = client.get(
        "/species/summary/datasheet/",
        {"period": "5", "subject": "Canis lupus", "region": ""},
    )
    assert "Secret Name" not in resp.html.name
