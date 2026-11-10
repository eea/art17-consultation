import urllib.parse

import pytest

from art17 import models
from art17.utils import sanitize_html

from .conftest import create_user, force_login
from .factories import CommentFactory, SpeciesManualAssessmentFactory

COMMENTS_URL = (
    urllib.parse.quote("/species/comments/6/Canis lupus/BOR/someuser/") + "?MS=EU27"
)


@pytest.fixture
def setup(app):
    SpeciesManualAssessmentFactory()
    CommentFactory()
    models.db.session.commit()


@pytest.mark.parametrize(
    "html, expected",
    [
        ("<p>ok</p><script>alert(1)</script>", "<p>ok</p>"),
        ('<p onclick="alert(1)">hi</p><img src=x onerror=alert(1)>', "<p>hi</p>"),
        ('<a href="javascript:alert(1)">x</a>', '<a rel="noopener noreferrer">x</a>'),
        (
            '<span style="background:url(http://evil);color:red">t</span>',
            '<span style="color:red">t</span>',
        ),
        (
            "<!--[if gte mso 9]><xml><w:WordDocument>Normal</w:WordDocument></xml>"
            '<![endif]--><p style="text-align:justify"><strong>Word</strong></p>',
            '<p style="text-align:justify"><strong>Word</strong></p>',
        ),
        (
            '<ul><li><a href="https://eea.europa.eu" target="_blank">link</a></li></ul>',
            '<ul><li><a href="https://eea.europa.eu" target="_blank" '
            'rel="noopener noreferrer">link</a></li></ul>',
        ),
        (None, ""),
    ],
)
def test_sanitize_html(html, expected):
    assert sanitize_html(html) == expected


def test_comment_sanitized_on_save(app, client, setup, set_auth):
    user = create_user("newuser")
    force_login(client, user.fs_uniquifier)

    client.post(COMMENTS_URL, {"comment": "<p>Hello</p><script>alert(1)</script>"})

    comment = models.Comment.query.filter_by(author_id="newuser").one()
    assert comment.comment == "<p>Hello</p>"


def test_stored_comment_sanitized_on_render(app, client, setup, set_auth):
    models.Comment.query.one().comment = "<p>Legacy</p><script>alert(1)</script>"
    models.db.session.commit()
    user = create_user("adminuser", ["admin"])
    force_login(client, user.fs_uniquifier)

    resp = client.get(COMMENTS_URL)

    assert "<p>Legacy</p>" in resp.text
    assert "alert(1)" not in resp.text


def test_csrf_token_required(app, client, setup, set_auth):
    app.config["WTF_CSRF_ENABLED"] = True
    user = create_user("newuser")
    force_login(client, user.fs_uniquifier)

    resp = client.post(COMMENTS_URL, {"comment": "<p>Forged</p>"}, expect_errors=True)
    assert resp.status_code == 400

    form = client.get(COMMENTS_URL).forms["theform"]
    form["comment"] = "<p>Genuine</p>"
    assert form.submit().status_code == 302
    assert models.Comment.query.filter_by(author_id="newuser").count() == 1


def test_csrf_over_https_without_referrer(app, client, setup, set_auth):
    # production sends "Referrer-Policy: no-referrer", so browsers omit Referer
    app.config["WTF_CSRF_ENABLED"] = True
    https = {"wsgi.url_scheme": "https"}
    user = create_user("newuser")
    force_login(client, user.fs_uniquifier)

    form = client.get(COMMENTS_URL, extra_environ=https).forms["theform"]
    # client.post (unlike form.submit) does not add a Referer header
    resp = client.post(
        COMMENTS_URL,
        {"csrf_token": form["csrf_token"].value, "comment": "<p>Genuine</p>"},
        extra_environ=https,
    )

    assert "Referer" not in resp.request.headers
    assert resp.status_code == 302
