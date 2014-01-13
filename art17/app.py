import flask
from flask.ext.script import Manager

from models import db, db_manager
from art17.views import summary
from art17.auth import auth
from assets import assets_env


DEFAULT_CONFIG = {
    'WTF_CSRF_ENABLED': False,
}


def create_app():
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.update(DEFAULT_CONFIG)
    app.config.from_pyfile('settings.py')
    assets_env.init_app(app)
    db.init_app(app)
    app.register_blueprint(summary)
    app.register_blueprint(auth)
    return app


def create_manager(app):
    manager = Manager(app)
    manager.add_command('db', db_manager)
    return manager
