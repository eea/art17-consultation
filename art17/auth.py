import flask
from flask.ext.principal import Principal, Identity, RoleNeed, UserNeed
import requests

auth = flask.Blueprint('auth', __name__)

principals = Principal(use_sessions=False)


@auth.record
def setup_auth_handlers(state):
    app = state.app
    principals.init_app(app)

    if app.config.get('AUTH_DEBUG'):
        DebugAuthProvider().init_app(app)

    if app.config.get('AUTH_ZOPE'):
        ZopeAuthProvider().init_app(app)


class DebugAuthProvider(object):

    def init_app(self, app):
        app.before_request(self.before_request_handler)
        app.add_url_rule(
            '/auth_debug',
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
            identity = Identity(id=auth_data['user_id'], auth_type='debug')
            principals.set_identity(identity)

            identity.provides.add(UserNeed(identity.id))
            for role_name in auth_data.get('roles', []):
                identity.provides.add(RoleNeed(role_name))

    def view(self):
        auth_debug_allowed = bool(flask.current_app.config.get('AUTH_DEBUG'))
        if flask.request.method == 'POST':
            if not auth_debug_allowed:
                flask.abort(403)
            user_id = flask.request.form['user_id']
            if user_id:
                roles = flask.request.form['roles'].strip().split()
                flask.session['auth'] = {'user_id': user_id, 'roles': roles}
            else:
                flask.session.pop('auth', None)
            return flask.redirect(flask.url_for('.debug'))

        roles = flask.session.get('auth', {}).get('roles', [])
        return flask.render_template('auth_debug.html', **{
            'user_id': flask.g.identity.id,
            'roles_txt': ''.join('%s\n' % r for r in roles),
            'auth_debug_allowed': auth_debug_allowed,
        })


class ZopeAuthProvider(object):

    def init_app(self, app):
        self.whoami_url = app.config['AUTH_ZOPE_WHOAMI_URL']
        app.before_request(self.before_request_handler)
        app.context_processor(lambda: {
            'art17_auth_zope': True,
        })

    def before_request_handler(self):
        auth_header = flask.request.headers.get('Authorization')
        resp = requests.get(
            self.whoami_url,
            headers={'Authorization': auth_header},
        )
        user_id = resp.json()['user_id']
        if user_id:
            identity = Identity(id=user_id, auth_type='zope')
            principals.set_identity(identity)
            identity.provides.add(UserNeed(identity.id))
