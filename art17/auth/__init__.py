import flask
from flask_login import LoginManager
from flask_security import Security

from art17.auth.providers import DebugAuthProvider
from art17.auth.security import Art17ForgotPasswordForm, UserDatastore, current_user
from art17.common import HOMEPAGE_VIEW_NAME
from art17.models import RegisteredUser, Role, db

auth = flask.Blueprint("auth", __name__)

login_manager = LoginManager()


@auth.record
def setup_auth_handlers(state):
    app = state.app

    if app.config.get("AUTH_DEBUG"):
        DebugAuthProvider().init_app(app)

    app.config.update(
        {
            "SECURITY_CONFIRMABLE": True,
            "SECURITY_POST_CONFIRM_VIEW": HOMEPAGE_VIEW_NAME,
            "SECURITY_PASSWORD_HASH": "ldap_salted_sha1",
            "SECURITY_PASSWORD_HASH": "ldap_salted_sha1",
            "SECURITY_PASSWORD_SCHEMES": ["ldap_salted_sha1"],
            "SECURITY_PASSWORD_SINGLE_HASH": ["ldap_salted_sha1"],
            "SECURITY_PASSWORD_SALT": "salted",
            "SECURITY_SEND_PASSWORD_CHANGE_EMAIL": True,
            "SECURITY_EMAIL_SUBJECT_REGISTER": (
                "Please confirm your email address for "
                "the Biological Diversity website"
            ),
            "SECURITY_MSG_EMAIL_CONFIRMED": (
                (
                    "Your email has been confirmed. You can now log in by "
                    "clicking the link at the top."
                ),
                "success",
            ),
            "SECURITY_RECOVERABLE": True,
            "SECURITY_RESET_URL": "/auth/recover_password",
            "SECURITY_POST_LOGIN_VIEW": HOMEPAGE_VIEW_NAME,
            "SECURITY_MSG_PASSWORD_RESET": (
                "You have successfully reset your password.",
                "success",
            ),
            "SECURITY_RESET_PASSWORD_TEMPLATE": "auth/reset_password_local.html",
            "SECURITY_POST_RESET_VIEW": HOMEPAGE_VIEW_NAME,
            "SECURITY_FORGOT_PASSWORD_TEMPLATE": "auth/forgot_password.html",
        }
    )

    app.jinja_env.globals["AUTH_BLUEPRINT_INSTALLED"] = True
    Security(
        datastore=UserDatastore(
            db,
            RegisteredUser,
            Role,
        ),
        app=app,
    )

    security_state = app.extensions["security"]
    security_state.pwd_context.update(ldap_salted_sha1__salt_size=7)
    security_state.forgot_password_form = Art17ForgotPasswordForm


import art17.auth.views  # make sure views get registered on the blueprint
