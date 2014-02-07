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
from art17.common import common
from art17.wiki import wiki
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
    if not app.testing:
        app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(common)
    app.register_blueprint(wiki)
    Mail().init_app(app)

    @app.route('/temp.html')
    def temp():
        return flask.render_template('temp.html')

    url_prefix = app.config.get('URL_PREFIX')
    if url_prefix:
        app.wsgi_app = create_url_prefix_middleware(app.wsgi_app, url_prefix)

    return app


def create_url_prefix_middleware(wsgi_app, url_prefix):
    def middleware(environ, start_response):
        path_info = environ['PATH_INFO']
        if path_info.startswith(url_prefix):
            environ['PATH_INFO'] = path_info[len(url_prefix):]
            environ['SCRIPT_NAME'] += url_prefix
        return wsgi_app(environ, start_response)
    return middleware


def create_manager(app):
    manager = Manager(app)
    manager.add_command('db', db_manager)
    manager.add_command('dataset', dataset_manager)
    manager.add_command('user', user_manager)
    manager.add_command('role', role_manager)
    return manager
