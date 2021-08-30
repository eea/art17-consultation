import logging
import requests

import flask

from art17 import models
from art17.auth.security import current_user

logger = logging.getLogger(__name__)


def set_user(user_id, is_ldap_user=False):
    user = models.RegisteredUser.query.get(user_id)
    flask.g.user_credentials = {
        "user_id": user_id,
        "is_ldap_user": is_ldap_user,
    }
    if user is None:
        logger.warning("Autheticated user %r not found in database", user_id)
    elif user.is_ldap != is_ldap_user:
        logger.warning(
            "Mix-up between LDAP and non-LDAP users: " "Ldap says %r, database says %r",
            is_ldap_user,
            user.is_ldap,
        )
    else:
        if user.is_active():
            flask.g.user = user
        else:
            logger.warning("User %r is marked as inactive", user_id)


class DebugAuthProvider(object):
    def init_app(self, app):
        app.before_request(self.before_request_handler)
        app.add_url_rule(
            "/auth/debug",
            endpoint="auth.debug",
            methods=["GET", "POST"],
            view_func=self.view,
        )
        app.context_processor(
            lambda: {
                "art17_auth_debug": True,
            }
        )

    def before_request_handler(self):
        user_id = flask.session.get("user_id")
        if user_id:
            user = models.RegisteredUser.query.get(user_id)
            if user:
                set_user(user_id=user_id, is_ldap_user=user.is_ldap)

    def view(self):
        auth_debug_allowed = bool(flask.current_app.config.get("AUTH_DEBUG"))
        if flask.request.method == "POST":
            if not auth_debug_allowed:
                flask.abort(403)
            user_id = flask.request.form["user_id"]
            if user_id:
                flask.session["auth"] = {"user_id": user_id}
            else:
                flask.session.pop("auth", None)
            return flask.redirect(flask.url_for(".debug"))

        return flask.render_template(
            "auth/debug.html",
            **{
                "user_id": current_user.get_id(),
                "auth_debug_allowed": auth_debug_allowed,
            }
        )
