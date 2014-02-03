import flask
from flask.ext.webtest import TestApp
from pytest import fixture
from alembic import command, config
from path import path
from mock import patch

from art17.app import create_app
from art17.models import db


TEST_CONFIG = {
    'SERVER_NAME': 'localhost',
    'SECRET_KEY': 'test',
    'ASSETS_DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@localhost/art17test',
}


alembic_cfg_path = path(__file__).dirname() / '..' / 'alembic.ini'
alembic_cfg = config.Config(alembic_cfg_path.abspath())


def create_db(url, db_name):
    conn = db.create_engine(url).connect()
    conn.execute('drop schema if exists %s' % db_name)
    conn.execute('create schema %s CHARACTER SET utf8 COLLATE utf8_general_ci'
                 % db_name)
    conn.close()


def drop_db(url, db_name):
    conn = db.create_engine(url).connect()
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

    app_context = app.app_context()
    app_context.push()

    parts = app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/')
    url, db_name = '/'.join(parts[:-1]), parts[-1]

    create_db(url, db_name)
    command.upgrade(alembic_cfg, 'head')

    @request.addfinalizer
    def fin():
        db.session.rollback()
        drop_db(url, db_name)
        app_context.pop()
    return app


@fixture
def client(app):
    client = TestApp(app, db=db, use_session_scopes=True)
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
    ldap_patch = patch('art17.auth.security.get_ldap_user_info')
    mock = ldap_patch.start()
    request.addfinalizer(ldap_patch.stop)
    mock.side_effect = library.get
    return library
