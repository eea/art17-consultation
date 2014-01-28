import logging
from datetime import datetime
import flask
from werkzeug.local import LocalProxy
from wtforms import TextField
from flask.ext.script import Manager, Option
from flask.ext.security import Security, SQLAlchemyUserDatastore, AnonymousUser
from flask.ext.security import core as flask_security_core
from flask.ext.security import views as flask_security_views
from flask.ext.security.forms import (
    ConfirmRegisterForm,
    password_length,
    Required,
)
from flask.ext.security.registerable import register_user
from flask.ext.security.script import (
    CreateUserCommand as BaseCreateUserCommand,
    CreateRoleCommand,
    AddRoleCommand,
    RemoveRoleCommand,
    DeactivateUserCommand,
    ActivateUserCommand,
)
from flask.ext.security import signals as security_signals
from flask.ext.mail import Message
import requests
from art17 import models

logger = logging.getLogger(__name__)

current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security_core.current_user = current_user
flask_security_views.current_user = current_user
flask_security_views.logout_user = lambda: None
flask_security_views.login_user = lambda new_user: None
flask_security_core._get_login_manager = lambda app: None
password_length.min = 1


@security_signals.user_confirmed.connect
def notify_administrator(app, user, **extra):
    msg = Message(
        subject="User has registered",
        sender=app.extensions['security'].email_sender,
        recipients=[app.config['AUTH_ADMIN_EMAIL']],
    )
    msg.body = flask.render_template(
        'auth/email_activate_user.txt',
        activation_link=flask.url_for(
            'auth.admin_user',
            user_id=user.id,
            _external=True,
        ),
    )
    app.extensions['mail'].send(msg)


class UserDatastore(SQLAlchemyUserDatastore):

    def create_user(self, **kwargs):
        del kwargs['password']
        kwargs.setdefault('active', False)
        kwargs['account_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, user, role):
        return (self.find_user(id=user), self.find_role(role))


class Art17ConfirmRegisterForm(ConfirmRegisterForm):

    id = TextField('id', validators=[Required("User ID is required")])


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

    app.config.update({
        'SECURITY_CONFIRMABLE': True,
        'SECURITY_REGISTERABLE': True,
    })

    security.init_app(
        app,
        confirm_register_form=Art17ConfirmRegisterForm,
    )


@auth.route('/auth/admin/<user_id>', methods=['GET', 'POST'])
def admin_user(user_id):
    user = models.RegisteredUser.query.get_or_404(user_id)
    if flask.request.method == 'POST':
        user.active = flask.request.form.get('active', type=bool)
        models.db.session.commit()
        flask.flash("User information updated for %s" % user_id, 'success')
        return flask.redirect(flask.url_for('.admin_user', user_id=user_id))

    return flask.render_template('auth/admin_user.html', user=user)


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
