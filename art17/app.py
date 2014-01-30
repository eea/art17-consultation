import flask
from flask.ext.script import Manager
from flask.ext.mail import Mail

from models import db, db_manager
from art17.layout import layout
from art17.summary import summary
from art17.progress import progress
from art17.report import report
from art17.auth import auth
from art17.comments import comments
from art17.auth.script import user_manager, role_manager
from art17.dataset import dataset_manager
from assets import assets_env


DEFAULT_CONFIG = {
    'WTF_CSRF_ENABLED': False,
}


def create_app(config={}, testing=False):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.update(DEFAULT_CONFIG)
    if testing:
        app.testing = True
    else:
        app.config.from_pyfile('settings.py')
    app.config.update(config)
    assets_env.init_app(app)
    db.init_app(app)
    app.register_blueprint(layout)
    app.register_blueprint(summary)
    app.register_blueprint(report)
    app.register_blueprint(progress)
    app.register_blueprint(auth)
    app.register_blueprint(comments)
    Mail().init_app(app)
    return app


def create_manager(app):
    manager = Manager(app)
    manager.add_command('db', db_manager)
    manager.add_command('dataset', dataset_manager)
    manager.add_command('user', user_manager)
    manager.add_command('role', role_manager)
    return manager
