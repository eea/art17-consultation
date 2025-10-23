import urllib
import uuid
import os
from datetime import date, datetime
from sqlalchemy.sql import text

import flask
from alembic import config
from flask_webtest import TestApp
from mock import patch
from path import Path
from pytest import fixture

from art17 import models
from art17.app import create_app

TEST_CONFIG = {
    "SERVER_NAME": "localhost",
    "SECRET_KEY": "test",
    "ASSETS_DEBUG": True,
    "EEA_LDAP_SERVER": "test_ldap_server",
    "EEA_PASSWORD_RESET": "",
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    # "SQLALCHEMY_BINDS":
    "SQLALCHEMY_BINDS": {
        "factsheet": "sqlite:///:memory:",
    },
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
}


alembic_cfg_path = Path((__file__)).dirname() / ".." / "alembic.ini"
alembic_cfg = config.Config(os.path.abspath(alembic_cfg_path))


def create_generic_fixtures():
    models.db.drop_all()
    models.db.create_all()
    models.db.session.execute(
        text(
            "insert into roles (name, description) " "values ('admin', 'Administrator')"
        )
    )
    models.db.session.execute(
        text(
            "insert into roles (name, description) "
            "values ('etc', 'European topic center')"
        )
    )
    models.db.session.execute(
        text(
            "insert into roles (name, description) "
            "values ('stakeholder', 'Stakeholder')"
        )
    )
    models.db.session.execute(
        text(
            "insert into roles (name, description) " "values ('nat', 'National expert')"
        )
    )
    models.db.session.execute(
        text(
            "insert into config(default_dataset_id, start_date) values (5, '%s')"
            % date.today()
        )
    )


def create_testing_app():
    app = create_app()
    test_config = dict(TEST_CONFIG)
    app = create_app(test_config, testing=True)
    return app


@fixture
def app(request):
    app = create_testing_app()

    @app.before_request
    def set_identity():
        from flask_principal import AnonymousIdentity

        flask.g.identity = AnonymousIdentity()

    app_context = app.app_context()
    app_context.push()
    create_generic_fixtures()

    @request.addfinalizer
    def fin():
        app_context.pop()

    return app


@fixture
def client(app):
    client = TestApp(app, db=models.db)
    return client


@fixture
def outbox(app, request):
    outbox_ctx = app.extensions["mail"].record_messages()

    @request.addfinalizer
    def cleanup():
        outbox_ctx.__exit__(None, None, None)

    return outbox_ctx.__enter__()


@fixture
def ldap_user_info(request):
    library = {}
    ldap_patch = patch("art17.auth.common.UsersDB")
    mock = ldap_patch.start()
    mock.return_value.user_info.side_effect = library.get
    request.addfinalizer(ldap_patch.stop)
    return library


@fixture
def set_auth(app, request):
    from art17.auth import auth

    app.register_blueprint(auth)

    requests_patch = patch("art17.auth.providers.requests")
    requests = requests_patch.start()
    request.addfinalizer(requests_patch.stop)

    whoami_data = {"user_id": None, "is_ldap_user": False}
    requests.get.return_value.json.return_value = whoami_data

    return whoami_data


def create_user(user_id, role_names=[], name="", institution="", ms=""):
    user = models.RegisteredUser(
        id=user_id,
        account_date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        active=True,
        name=name,
        email="%s@example.com" % user_id,
        institution=institution,
        MS=ms,
        fs_uniquifier=f"{user_id}_fs",
    )
    models.db.session.add(user)
    for name in role_names:
        role = models.Role.query.filter_by(name=name).first()
        user.roles.append(role)
    models.db.session.commit()

    return user


def get_request_params(request_type, request_args, post_params=None):
    request_args[0] = urllib.parse.quote(request_args[0])
    if request_type == "post":
        query_string = urllib.parse.urlencode(request_args[1])
        final_url = "?".join((request_args[0], query_string))
        request_args = [final_url, post_params]
    return request_args


def force_login(client, fs_uniquifier=None):
    with client.session_transaction() as sess:
        sess["_user_id"] = fs_uniquifier
        sess["_fresh"] = True
