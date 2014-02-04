from datetime import datetime
from functools import wraps
import flask
from flask.ext.principal import PermissionDenied
from flask.ext.security import Security
from flask.ext.security import signals as security_signals
from flask.ext.mail import Message
from art17.auth.security import (
    UserDatastore,
    Art17ConfirmRegisterForm,
    current_user,
)
from art17 import models
from art17.auth.providers import DebugAuthProvider, ZopeAuthProvider
from art17.common import admin_perm

HOMEPAGE_VIEW_NAME = 'summary.homepage'


@security_signals.user_confirmed.connect
def notify_administrator(app, user, **extra):
    msg = Message(
        subject="User has registered",
        sender=app.extensions['security'].email_sender,
        recipients=[app.config['AUTH_ADMIN_EMAIL']],
    )
    msg.body = flask.render_template(
        'auth/email_admin_new_user.txt',
        user=user,
        activation_link=flask.url_for(
            'auth.admin_user',
            user_id=user.id,
            _external=True,
        ),
    )
    app.extensions['mail'].send(msg)

auth = flask.Blueprint('auth', __name__)
security_ext = Security(
    datastore=UserDatastore(
        models.db,
        models.RegisteredUser,
        models.Role,
    ),
)


def require_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        admin_perm.test()
        return view(*args, **kwargs)
    return wrapper


def get_ldap_user_info(user_id):
    from eea.usersdb import UsersDB
    ldap_server = flask.current_app.config['EEA_LDAP_SERVER']
    users_db = UsersDB(ldap_server=ldap_server)
    return users_db.user_info(user_id)


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
        'SECURITY_REGISTER_URL': '/auth/register/local',
        'SECURITY_POST_CONFIRM_VIEW': HOMEPAGE_VIEW_NAME,
    })

    security_ext.init_app(
        app,
        confirm_register_form=Art17ConfirmRegisterForm,
    )


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = flask.render_template('auth/permission_denied.html')
    return flask.Response(html, status=403)


def set_user_active(user, new_active):
    was_active = user.active
    user.active = new_active
    models.db.session.commit()
    if not user.is_ldap:
        if was_active and not new_active:
            zope_acl_manager.delete(user)
        if new_active and not was_active:
            zope_acl_manager.create(user)


@auth.route('/auth/admin/<user_id>', methods=['GET', 'POST'])
@require_admin
def admin_user(user_id):
    user = models.RegisteredUser.query.get_or_404(user_id)
    if flask.request.method == 'POST':
        set_user_active(user, flask.request.form.get('active', type=bool))
        flask.flash("User information updated for %s" % user_id, 'success')
        return flask.redirect(flask.url_for('.admin_user', user_id=user_id))

    return flask.render_template('auth/admin_user.html', user=user)


@auth.route('/auth/register')
def register():
    user_credentials = flask.g.get('user_credentials', {})
    if user_credentials.get('is_ldap_user'):
        return flask.redirect(flask.url_for('.register_ldap'))

    return flask.render_template('auth/register_choices.html')


@auth.route('/auth/register/ldap', methods=['GET', 'POST'])
def register_ldap():
    user_credentials = flask.g.get('user_credentials', {})
    if not user_credentials.get('is_ldap_user'):
        return flask.redirect(flask.url_for('.register'))

    if flask.request.method == 'POST':
        datastore = flask.current_app.extensions['security'].datastore
        ldap_user_info = get_ldap_user_info(user_credentials['user_id'])
        user = datastore.create_user(
            id=user_credentials['user_id'],
            is_ldap=True,
            password='',
            confirmed_at=datetime.utcnow(),
            email=ldap_user_info.get('email'),
        )
        datastore.commit()
        flask.flash(
            "Eionet account %s has been activated"
            % user_credentials['user_id'],
            'success',
        )
        notify_administrator(flask._app_ctx_stack.top.app, user)
        return flask.render_template('auth/register_ldap_done.html')

    return flask.render_template('auth/register_ldap.html', **{
        'already_registered': flask.g.get('user') is not None,
        'user_id': user_credentials['user_id'],
    })
