import flask
from flask.ext.security import Security
from art17.auth.security import (
    UserDatastore,
    Art17ConfirmRegisterForm,
    current_user,
)
from art17.auth.providers import DebugAuthProvider, ZopeAuthProvider
from art17 import models
from art17.common import HOMEPAGE_VIEW_NAME


auth = flask.Blueprint('auth', __name__)
security_ext = Security(
    datastore=UserDatastore(
        models.db,
        models.RegisteredUser,
        models.Role,
    ),
)


@auth.record
def setup_auth_handlers(state):
    app = state.app

    if app.config.get('AUTH_DEBUG'):
        DebugAuthProvider().init_app(app)

    if app.config.get('AUTH_ZOPE'):
        ZopeAuthProvider().init_app(app)

    app.config.update({
        'SECURITY_CONFIRMABLE': True,
        'SECURITY_POST_CONFIRM_VIEW': HOMEPAGE_VIEW_NAME,
        'SECURITY_PASSWORD_HASH': 'ldap_salted_sha1',
        'SECURITY_SEND_PASSWORD_CHANGE_EMAIL': False,
    })

    app.jinja_env.globals['AUTH_BLUEPRINT_INSTALLED'] = True

    security_ext.init_app(
        app,
        confirm_register_form=Art17ConfirmRegisterForm,
    )

    pwd_context = app.extensions['security'].pwd_context
    pwd_context.update(ldap_salted_sha1__salt_size=7)


import art17.auth.views  # make sure views get registered on the blueprint
