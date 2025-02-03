import os

import flask
import pytest
from mock import patch
from flask_webtest import TestApp
from art17 import models

from .conftest import create_user, force_login


def _set_config(**kwargs):
    from art17.common import get_config
    from art17.models import db

    for key in kwargs:
        setattr(get_config(), key, kwargs[key])
    db.session.commit()


def test_identity_is_set_from_plone_whoami(app, set_auth, client):
    user_obj = create_user("ze_admin", ["admin"])

    @app.route("/identity")
    def get_identity():
        identity = flask.g.identity
        return flask.jsonify(
            id=identity.id,
            provides=sorted(list(identity.provides)),
        )

    force_login(client, user_obj.fs_uniquifier)

    identity = client.get("/identity").json
    assert identity["id"] == user_obj.fs_uniquifier
    assert identity["provides"] == [
        ["id", user_obj.fs_uniquifier],
        ["role", "admin"],
    ]


def test_self_registration_flow(app, set_auth, client, outbox, ldap_user_info):
    
    from .factories import DatasetFactory
    _set_config(admin_email="admin@example.com")
    user_obj = create_user("ze_admin", ["admin"])
    fs_uniquifier = user_obj.fs_uniquifier
    DatasetFactory()
    models.db.session.commit()

    register_page = client.get(flask.url_for("auth.register_local"))
    register_page.form["id"] = "foo"
    register_page.form["email"] = "foo@example.com"
    register_page.form["password"] = "p455w4rd"
    register_page.form["name"] = "foo me"
    register_page.form["institution"] = "foo institution"
    result_page = register_page.form.submit()
    assert "Thank you. To confirm your email address foo@example.com, please click on the link in the email we have just sent to you" in result_page.text

    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is None
    assert not foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith("{SSHA}")

    assert len(outbox) == 1
    confirm_message = outbox.pop()
    assert "Dear foo me," in confirm_message.body
    assert "foo@example.com" in confirm_message.body
    url = confirm_message.body.splitlines()[4].strip()
    assert url.startswith("http://localhost/confirm/")

    client.get(url)
    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.confirmed_at is not None
    assert foo_user.active

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ["admin@example.com"]
    assert "Local user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == "http://localhost/auth/users/foo"

    # force_login(client, fs_uniquifier)
    # activation_page = client2.get(url)
    # activation_page.form["active"] = False
    # activation_page.form.submit()

    # foo_user = models.RegisteredUser.query.get("foo")
    # assert not foo_user.active


def test_admin_creates_local(app, set_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    user_obj = create_user("ze_admin", ["admin"])
    force_login(client, user_obj.fs_uniquifier)
    DatasetFactory()
    models.db.session.commit()

    register_page = client.get(flask.url_for("auth.admin_create_local"))
    register_page.form["id"] = "foo"
    register_page.form["email"] = "foo@example.com"
    register_page.form["password"] = "p455w4rd"
    register_page.form["name"] = "foo me"
    register_page.form["institution"] = "foo institution"

    result_page = register_page.form.submit().follow()

    assert "User foo created successfully." in result_page

    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith("{SSHA}")

    assert len(outbox) == 1
    message = outbox.pop()
    assert "Dear foo me," in message.body
    assert '"foo"' in message.body
    assert '"p455w4rd"' in message.body


def test_admin_creates_ldap(app, set_auth, client, outbox, ldap_user_info):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    user_obj = create_user("ze_admin", ["admin"])
    force_login(client, user_obj.fs_uniquifier)
    DatasetFactory()
    models.db.session.commit()

    ldap_user_info["foo"] = {
        "full_name": "foo me",
        "email": "foo@example.com",
    }

    enter_user_id_page = client.get(flask.url_for("auth.admin_create_ldap"))
    enter_user_id_page.form["user_id"] = "foo"
    register_page = enter_user_id_page.form.submit()

    register_page.form["institution"] = "foo institution"

    result_page = register_page.form.submit().follow()

    assert "User foo created successfully." in result_page

    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    message = outbox.pop()
    assert "Dear foo me," in message.body
    assert '"foo"' in message.body


@pytest.mark.skipif(True, reason="always skip")
# the workflow should probably be removed as the user is now
# registered and activated on the first ldap login
def test_ldap_account_activation_flow(app, set_auth, client, outbox, ldap_user_info):
    from art17.auth.providers import set_user

    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    ldap_user_info["foo"] = {"email": "foo@example.com", "full_name": "foo"}
    user_obj = create_user("ze_admin", ["admin"])
    DatasetFactory()
    models.db.session.commit()

    @app.before_request
    def set_testing_user():
        set_user("foo", is_ldap_user=True)

    register_page = client.get(flask.url_for("auth.register_ldap"))
    register_page.form["institution"] = "foo institution"

    result_page = register_page.form.submit()
    assert "has been registered" in result_page.text

    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ["admin@example.com"]
    assert "Eionet user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == "http://localhost/auth/users/foo"

    force_login(client, user_obj.fs_uniquifier)
    activation_page = client.get(url)
    activation_page.form["active"] = False
    activation_page.form.submit()

    foo_user = models.RegisteredUser.query.get("foo")
    assert not foo_user.active


def test_view_requires_admin_error(app, set_auth, client):
    from .factories import DatasetFactory
    create_user("foo")
    user_obj = create_user("ze_admin", ["admin"])
    DatasetFactory()
    models.db.session.commit()
    admin_user_url = flask.url_for("auth.admin_user", user_id="foo")

def test_view_requires_admin(app, set_auth, client):
    from .factories import DatasetFactory
    create_user("foo")
    user_obj = create_user("ze_admin", ["admin"])
    DatasetFactory()
    models.db.session.commit()
    admin_user_url = flask.url_for("auth.admin_user", user_id="foo")
    force_login(client, user_obj.fs_uniquifier)
    assert client.get(admin_user_url).status_code == 200


def test_change_local_password(app, set_auth, client):
    from flask_security.utils import encrypt_password

    foo = create_user("foo")
    old_enc_password = encrypt_password("my old pw")
    foo.password = old_enc_password
    models.db.session.commit()

    set_auth.update({"user_id": "foo"})
    force_login(client, foo.fs_uniquifier)
    page = client.get(flask.url_for("auth.change_password"))
    page.form["password"] = "my old pw"
    page.form["new_password"] = "the new pw"
    page.form["new_password_confirm"] = "the new pw"
    confirmation_page = page.form.submit().follow()

    assert "password has been changed" in confirmation_page.text

    foo = models.RegisteredUser.query.filter_by(id="foo").first()
    assert foo.password != old_enc_password


def test_change_anonymous_password(app, set_auth, client):
    page = client.get(flask.url_for("auth.change_password"))
    assert "You must log in before changing your password" in page


def test_change_ldap_password(app, set_auth, client):
    foo = create_user("foo")
    foo.is_ldap = True
    models.db.session.commit()
    force_login(client, foo.fs_uniquifier)
    page = client.get(flask.url_for("auth.change_password"))
    assert os.environ.get("EEA_PASSWORD_RESET") in page


def test_dates(app, set_auth, client):
    from datetime import date, timedelta

    today = date.today()

    _set_config(
        start_date=today + timedelta(days=2),
        end_date=today + timedelta(days=4),
    )
    page = client.get(flask.url_for("auth.register_ldap"))
    assert "Registration has not started yet" in page

    _set_config(
        start_date=today - timedelta(days=4),
        end_date=today - timedelta(days=2),
    )
    page = client.get(flask.url_for("auth.register_ldap"))
    assert "Registration has finished" in page


def test_admin_edit_user_info(app, set_auth, client, outbox):
    from .factories import DatasetFactory

    _set_config(admin_email="admin@example.com")
    user_obj = create_user("ze_admin", ["admin"])
    create_user("foo", ["etc", "stakeholder"], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    force_login(client, user_obj.fs_uniquifier)

    page = client.get(flask.url_for("auth.admin_user", user_id="foo"))
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form["qualification"] = "Foo is web developer"
    result_page = page.form.submit()

    assert "User information updated" in result_page.follow().text
    assert not result_page.status_code == 200
    assert not "already associated with an account" in result_page.text

    foo_user = models.RegisteredUser.query.get("foo")
    assert foo_user.email == "foo@example.com"
    assert foo_user.name == "Foo Person"
    assert foo_user.institution == "Foo Institution"
    assert foo_user.qualification == "Foo is web developer"
    assert not foo_user.is_ldap

    create_user("bar", ["etc"], name="Bar Person")
    models.db.session.commit()

    page = client.get(flask.url_for("auth.admin_user", user_id="bar"))
    page.form["name"] = "Bar Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Bar Institution"
    page.form["qualification"] = "Bar is web developer"
    result_page = page.form.submit()

    assert result_page.status_code == 200
    assert "already associated with an account" in result_page.text


def test_email_notification_for_role_changes(app, set_auth, client, outbox):
    from .factories import DatasetFactory

    user_obj = create_user("ze_admin", ["admin"])
    create_user("foo", ["etc", "stakeholder"], name="Foo Person")
    DatasetFactory()
    models.db.session.commit()
    force_login(client, user_obj.fs_uniquifier)
    page = client.get(flask.url_for("auth.admin_user", user_id="foo"))
    page.form["roles"] = ["stakeholder", "nat"]
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form.submit()
    assert len(outbox) == 0

    page.form["roles"] = ["etc", "stakeholder"]
    page.form["name"] = "Foo Person"
    page.form["email"] = "foo@example.com"
    page.form["institution"] = "Foo Institution"
    page.form["notify_user"] = True
    page.form.submit()

    assert len(outbox) == 1
    [msg] = outbox
    assert msg.recipients == ["foo@example.com"]
    assert "* European topic center" in msg.body
    assert "* Stakeholder" in msg.body
