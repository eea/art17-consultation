import flask
from flask.ext.webtest import TestApp
from pytest import fixture
from alembic import command, config
from path import path
from mock import patch
from datetime import datetime

from art17.app import create_app
from art17 import models


TEST_CONFIG = {
    'SERVER_NAME': 'localhost',
    'SECRET_KEY': 'test',
    'ASSETS_DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@localhost/art17test',
    'EEA_LDAP_SERVER': 'test_ldap_server'
}


alembic_cfg_path = path(__file__).dirname() / '..' / 'alembic.ini'
alembic_cfg = config.Config(alembic_cfg_path.abspath())


def create_db(url, db_name):
    conn = models.db.create_engine(url).connect()
    conn.execute('drop schema if exists %s' % db_name)
    conn.execute('create schema %s CHARACTER SET utf8 COLLATE utf8_general_ci'
                 % db_name)
    conn.close()


def drop_db(url, db_name):
    conn = models.db.create_engine(url).connect()
    conn.execute('drop schema %s' % db_name)
    conn.close()


def create_testing_app():
    local_config = create_app().config

    test_config = dict(TEST_CONFIG)

    for name, value in local_config.iteritems():
        if name.startswith('TESTING_'):
            test_config[name[len('TESTING_'):]] = value

    app = create_app(test_config, testing=True)
    return app


@fixture
def app(request):
    app = create_testing_app()

    @app.before_request
    def set_identity():
        from flask.ext.principal import AnonymousIdentity
        flask.g.identity = AnonymousIdentity()

    app_context = app.app_context()
    app_context.push()

    parts = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/')
    url, db_name = '/'.join(parts[:-1]), parts[-1]

    create_db(url, db_name)
    command.upgrade(alembic_cfg, 'head')

    @request.addfinalizer
    def fin():
        models.db.session.rollback()
        drop_db(url, db_name)
        app_context.pop()
    return app


@fixture
def client(app):
    client = TestApp(app, db=models.db, use_session_scopes=True)
    return client


@fixture
def outbox(app, request):
    outbox_ctx = app.extensions['mail'].record_messages()

    @request.addfinalizer
    def cleanup():
        outbox_ctx.__exit__(None, None, None)

    return outbox_ctx.__enter__()


@fixture
def ldap_user_info(request):
    library = {}
    ldap_patch = patch('art17.auth.common.UsersDB')
    mock = ldap_patch.start()
    mock.return_value.user_info.side_effect = library.get
    request.addfinalizer(ldap_patch.stop)
    return library


@fixture
def zope_auth(app, request):
    from art17.auth import auth

    app.config['AUTH_ZOPE'] = True
    app.config['AUTH_ZOPE_WHOAMI_URL'] = 'http://example.com/'
    app.register_blueprint(auth)

    requests_patch = patch('art17.auth.providers.requests')
    requests = requests_patch.start()
    request.addfinalizer(requests_patch.stop)

    whoami_data = {'user_id': None, 'is_ldap_user': False}
    requests.get.return_value.json.return_value = whoami_data

    return whoami_data


def create_user(user_id, role_names=[]):
    user = models.RegisteredUser(
        id=user_id,
        account_date=datetime.utcnow(),
        active=True,
    )
    models.db.session.add(user)
    for name in role_names:
        role = models.Role.query.filter_by(name=name).first()
        user.roles.append(role)
    models.db.session.commit()

    return user
