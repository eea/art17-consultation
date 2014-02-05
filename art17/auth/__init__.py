from datetime import datetime
from functools import wraps
import flask
from flask.ext.principal import PermissionDenied
from flask.ext.security import Security
from flask.ext.security import signals as security_signals
from flask.ext.security.forms import ChangePasswordForm
from flask.ext.security.changeable import change_user_password
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
def put_in_activation_queue(app, user, **extra):
    user.waiting_for_activation = True
    models.db.session.commit()

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


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = flask.render_template('auth/permission_denied.html')
    return flask.Response(html, status=403)


def notify_user_account_activated(user):
    app = flask.current_app
    msg = Message(
        subject="Account has been activated",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = flask.render_template(
        'auth/email_user_activated.txt',
        user=user,
        home_url=flask.url_for(HOMEPAGE_VIEW_NAME),
    )
    app.extensions['mail'].send(msg)


def set_user_active(user, new_active):
    was_active = user.active
    user.active = new_active
    if user.waiting_for_activation and not was_active and new_active:
        user.waiting_for_activation = False
        notify_user_account_activated(user)
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
        put_in_activation_queue(flask._app_ctx_stack.top.app, user)
        return flask.render_template('auth/register_ldap_done.html')

    return flask.render_template('auth/register_ldap.html', **{
        'already_registered': flask.g.get('user') is not None,
        'user_id': user_credentials['user_id'],
    })


@auth.route('/auth/change_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_anonymous():
        message = "You must log in before changing your password."
        return flask.render_template('message.html', message=message)

    if current_user.is_ldap:
        message = "Please go to the EIONET account change password page."
        return flask.render_template('message.html', message=message)

    form = ChangePasswordForm()

    if form.validate_on_submit():
        change_user_password(current_user, form.new_password.data)
        models.db.session.commit()
        msg = "Your password has been changed. Please log in again."
        flask.flash(msg, 'success')
        zope_acl_manager.create(current_user)
        return flask.redirect(flask.url_for(HOMEPAGE_VIEW_NAME))

    return flask.render_template('auth/change_password.html', **{
        'form': form,
    })
