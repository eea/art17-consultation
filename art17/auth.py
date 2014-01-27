import logging
from datetime import datetime
import flask
from werkzeug.local import LocalProxy
from flask.ext.script import Manager, Option
from flask.ext.security import Security, SQLAlchemyUserDatastore, AnonymousUser
from flask.ext.security import core as flask_security_core
from flask.ext.security import forms as flask_security_forms
from flask.ext.security.script import (
    CreateUserCommand as BaseCreateUserCommand,
    CreateRoleCommand,
    AddRoleCommand,
    RemoveRoleCommand,
    DeactivateUserCommand,
    ActivateUserCommand,
)
import requests
from art17 import models

logger = logging.getLogger(__name__)

current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security_core.current_user = current_user
flask_security_core._get_login_manager = lambda app: None
flask_security_forms.password_length.min = 1


class UserDatastore(SQLAlchemyUserDatastore):

    def create_user(self, **kwargs):
        del kwargs['password']
        kwargs['account_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, user, role):
        return (self.find_user(id=user), self.find_role(role))


auth = flask.Blueprint('auth', __name__)
security = Security(
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

    security.init_app(app)


def set_user(user_id):
    user = models.RegisteredUser.query.get(user_id)
    if user is None:
        logger.warn("Autheticated user %r not found in database", user_id)
    else:
        if user.is_active():
            flask.g.user = user
        else:
            logger.warn("User %r is marked as inactive", user_id)


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

        return flask.render_template('auth_debug.html', **{
            'user_id': current_user.get_id(),
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
            set_user(user_id=user_id)


class CreateUserCommand(BaseCreateUserCommand):

    option_list = BaseCreateUserCommand.option_list + (
        Option('-i', '--id', dest='id', default=None),
    )

    def run(self, **kwargs):
        kwargs['password'] = 'foo'
        super(CreateUserCommand, self).run(**kwargs)


user_manager = Manager()
user_manager.add_command('create', CreateUserCommand())
user_manager.add_command('deactivate', DeactivateUserCommand())
user_manager.add_command('activate', ActivateUserCommand())


@user_manager.command
def ls():
    for user in models.RegisteredUser.query:
        print "{u.id} <{u.email}>".format(u=user)


@user_manager.command
def remove(user_id):
    user = models.RegisteredUser.query.get(user_id)
    models.db.session.delete(user)
    models.db.session.commit()


role_manager = Manager()
role_manager.add_command('create', CreateRoleCommand())
role_manager.add_command('add', AddRoleCommand())
role_manager.add_command('remove', RemoveRoleCommand())


@role_manager.command
def ls():
    for role in models.Role.query:
        print "{r.name}: {r.description}".format(r=role)


@role_manager.command
def members(role):
    role_ob = models.Role.query.filter_by(name=role).first()
    if role_ob is None:
        print 'No such role %r' % role
        return
    for user in role_ob.users:
        print "{u.id} <{u.email}>".format(u=user)
