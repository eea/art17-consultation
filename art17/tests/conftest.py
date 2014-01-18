from flask.ext.webtest import TestApp
from pytest import fixture
from alembic import command, config
from path import path

from art17.app import create_app
from art17.models import db


test_config = {
    'SERVER_NAME': 'localhost',
    'TESTING': True,
    'SECRET_KEY': 'test',
    'ASSETS_DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@localhost/art17testing',
    'SQLALCHEMY_MYSQL_URI': 'mysql://root@localhost/',
}


alembic_cfg_path = path(__file__).dirname() / '..' / '..' / 'alembic.ini'
alembic_cfg = config.Config(alembic_cfg_path.abspath())


def create_db(url):
    conn = db.create_engine(url).connect()
    conn.execute('drop schema if exists art17testing')
    conn.execute('create schema art17testing')
    conn.close()


def drop_db(url):
    conn = db.create_engine(url).connect()
    conn.execute('drop schema art17testing')
    conn.close()


@fixture
def app(request):
    app = create_app(test_config)
    app_context = app.app_context()
    app_context.push()

    create_db(app.config['SQLALCHEMY_MYSQL_URI'])
    command.upgrade(alembic_cfg, 'head')

    @request.addfinalizer
    def fin():
        drop_db(app.config['SQLALCHEMY_MYSQL_URI'])
        app_context.pop()
    return app


@fixture
def client(app):
    client = TestApp(app, db=db, use_session_scopes=True)
    return client
