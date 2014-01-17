import pytest
from art17.app import create_app
from art17.models import db


# self.client = TestApp(self.app, db=db, use_session_scopes=True)

CONFIG = {
    'TESTING': True,
    'SECRET_KEY': 'test',
    'ASSETS_DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'mysql://root@localhost/',
    'SQLALCHEMY_BINDS': {
        'testing': 'mysql://root@localhost/art17testing'
    }
}


def create_db(db):
    conn = db.engine.connect()
    conn.execute('drop schema if exists art17testing')
    conn.execute('create schema art17testing')
    conn.close()


def drop_db(db):
    conn = db.engine.connect()
    conn.execute('drop schema art17testing')
    conn.close()


@pytest.fixture(scope='module')
def app(request):
    app = create_app(CONFIG)
    with app.app_context():
        create_db(db)
        db.create_all(bind='testing')

    @request.addfinalizer
    def fin():
        with app.app_context():
            drop_db(db)
    return app
