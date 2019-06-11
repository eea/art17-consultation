import logging
import requests
import flask
from art17 import models
from art17.auth.security import current_user

logger = logging.getLogger(__name__)


def set_user(user_id, is_ldap_user=False):
    user = models.RegisteredUser.query.get(user_id)
    flask.g.user_credentials = {
        'user_id': user_id,
        'is_ldap_user': is_ldap_user,
    }
    if user is None:
        logger.warn("Autheticated user %r not found in database", user_id)
    elif user.is_ldap != is_ldap_user:
        logger.warn(
            "Mix-up between LDAP and non-LDAP users: "
            "Plone says %r, database says %r",
            is_ldap_user, user.is_ldap,
        )
    else:
        if user.is_active():
            flask.g.user = user
        else:
            logger.warn("User %r is marked as inactive", user_id)


class DebugAuthProvider(object):

    def init_app(self, app):
        app.before_request(self.before_request_handler)
        app.add_url_rule(
            '/auth/debug',
            endpoint='auth.debug',
            methods=['GET', 'POST'],
            view_func=self.view,
        )
        app.context_processor(lambda: {
            'art17_auth_debug': True,
        })

    def before_request_handler(self):
        auth_data = flask.session.get('auth')
        if auth_data and auth_data.get('user_id'):
            set_user(user_id=auth_data['user_id'])

    def view(self):
        auth_debug_allowed = bool(flask.current_app.config.get('AUTH_DEBUG'))
        if flask.request.method == 'POST':
            if not auth_debug_allowed:
                flask.abort(403)
            user_id = flask.request.form['user_id']
            if user_id:
                flask.session['auth'] = {'user_id': user_id}
            else:
                flask.session.pop('auth', None)
            return flask.redirect(flask.url_for('.debug'))

        return flask.render_template('auth/debug.html', **{
            'user_id': current_user.get_id(),
            'auth_debug_allowed': auth_debug_allowed,
        })


class PloneAuthProvider(object):

    def init_app(self, app):
        self.whoami_url = app.config['AUTH_PLONE_WHOAMI_URL']
        app.before_request(self.before_request_handler)
        app.context_processor(lambda: {
            'art17_auth_plone': True,
        })

    def before_request_handler(self):
        auth_cookie = flask.request.cookies.get('__ac')
        resp = requests.get(
            self.whoami_url,
            cookies={'__ac': auth_cookie},
            verify=False
        )
        try:
            resp_data = resp.json()
            if resp_data['user_id']:
                set_user(
                    user_id=resp_data['user_id'],
                    is_ldap_user=resp_data['is_ldap_user'],
                )
        except ValueError:
            pass