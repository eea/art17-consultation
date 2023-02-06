import logging
import logging.handlers

import flask
from flask_mail import Mail
from flask_migrate import Migrate

from art17.assets import assets_env
from art17.auth import auth, login_manager
from art17.auth.script import role_manager, user_manager
from art17.comments import comments
from art17.common import common
from art17.dataset import dataset_manager
from art17.factsheet import factsheet, factsheet_manager
from art17.layout import layout
from art17.management.fix_bg_cdr_link import fix_bg_link
from art17.management.fix_manual import fix_manual
from art17.management.generate_new_period import generate_new_period
from art17.management.import_greece import import_greece
from art17.management.import_new_data import import_new_data
from art17.management.pre_fill_wiki_changes_habitat import \
    pre_fill_wiki_changes_habitat
from art17.management.pre_fill_wiki_changes_species import \
    pre_fill_wiki_changes_species
from art17.maps import maps
from art17.models import db
from art17.progress import progress
from art17.report import report
from art17.summary import summary
from art17.utils import inject_static_file
from art17.wiki import wiki

DEFAULT_CONFIG = {
    "WTF_CSRF_ENABLED": False,
    "MAP_SERVICE_SPECIES": "http://nature-art17.eionet.europa.eu/article17/"
    "speciessummary/details/art17ws",
    "MAP_SERVICE_HABITATS": "https://nature-art17.eionet.europa.eu/article17/"
    "habitatsummary/details/art17ws",
    "PDF_DESTINATION": "factsheets",
    "PDF_URL_PREFIX": "",
    "FACTSHEET_DEFAULT_PERIOD": "1",
    "MAPS_STATIC": "",
    "MAPS_FORMAT": "map0{which}{type}/{code}_0{which}_{type}.png",
}


def configure_auth_log_hander(log_path):
    auth_logger = logging.getLogger("art17.auth")
    for handler in list(auth_logger.handlers):
        auth_logger.removeHandler(handler)
    handler = logging.handlers.RotatingFileHandler(
        log_path,
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=4,
    )
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(module)s %(levelname)s %(message)s",
        )
    )
    handler.setLevel(logging.INFO)
    auth_logger.addHandler(handler)


def create_app(config={}, testing=False):
    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.update(DEFAULT_CONFIG)
    if testing:
        app.testing = True
        app.config.from_pyfile("test_settings.py", silent=True)
    else:
        app.config.from_pyfile("settings.py")
    app.config.update(config)
    create_cli_commands(app)
    assets_env.init_app(app)
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(layout)
    app.register_blueprint(summary)
    app.register_blueprint(report)
    app.register_blueprint(progress)
    if not app.testing:
        app.register_blueprint(auth)
    app.register_blueprint(comments)
    app.register_blueprint(common)
    app.register_blueprint(wiki)
    app.register_blueprint(maps)
    app.register_blueprint(factsheet)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    Mail().init_app(app)
    app.add_template_global(inject_static_file)
    return app

    @app.route("/temp.html")
    def temp():
        return flask.render_template("temp.html")

    url_prefix = app.config.get("URL_PREFIX")
    if url_prefix:
        app.wsgi_app = create_url_prefix_middleware(app.wsgi_app, url_prefix)

    if app.config.get("SENTRY_DSN"):
        from raven.contrib.flask import Sentry

        Sentry(app)

    if app.config.get("AUTH_LOG_FILE"):
        configure_auth_log_hander(app.config.get("AUTH_LOG_FILE"))

    return app


def create_url_prefix_middleware(wsgi_app, url_prefix):
    def middleware(environ, start_response):
        path_info = environ["PATH_INFO"]
        if path_info.startswith(url_prefix):
            environ["PATH_INFO"] = path_info[len(url_prefix) :]
            environ["SCRIPT_NAME"] += url_prefix
        return wsgi_app(environ, start_response)

    return middleware


def create_cli_commands(app):
    app.cli.add_command(dataset_manager)
    app.cli.add_command(user_manager)
    app.cli.add_command(role_manager)
    app.cli.add_command(factsheet_manager)

    app.cli.add_command(import_greece)
    app.cli.add_command(generate_new_period)
    app.cli.add_command(fix_manual)
    app.cli.add_command(pre_fill_wiki_changes_habitat)
    app.cli.add_command(pre_fill_wiki_changes_species)
    app.cli.add_command(import_new_data)
    app.cli.add_command(fix_bg_link)
