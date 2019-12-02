import logging
import ldap
from datetime import date
from functools import wraps
import flask
from flask_security import signals as security_signals
from flask_mail import Message
from smtplib import SMTPException
from eea.usersdb import UsersDB, UserNotFound
from art17 import models
from art17.common import admin_perm, get_config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_ROLE = 'stakeholder'


def safe_send_mail(app, msg):
    try:
        app.extensions['mail'].send(msg)
    except SMTPException:
        flask.flash("The mail could not be sent to the specified email address."
                    "Please contact the administrator.")


@security_signals.user_confirmed.connect
def activate_and_notify_admin(app, user, **extra):
    set_user_active(user, True)
    models.db.session.commit()
    admin_email = get_config().admin_email

    if not admin_email:
        logger.warn("No admin_email is configured; not sending email")

    else:
        msg = Message(
            subject="User has registered",
            sender=app.extensions['security'].email_sender,
            recipients=admin_email.split(),
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
        safe_send_mail(app, msg)


def require_admin(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        admin_perm.test()
        return view(*args, **kwargs)
    return wrapper


def get_ldap_user_info(user_id):
    ldap_server = flask.current_app.config.get('EEA_LDAP_SERVER', '')
    users_db = UsersDB(ldap_server=ldap_server)
    try:
        return users_db.user_info(user_id)
    except UserNotFound:
        return None
    except ldap.INVALID_DN_SYNTAX:
        return None


def set_user_active(user, new_active):
    was_active = user.active
    user.active = new_active
    models.db.session.commit()


def check_dates(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        config = get_config()

        if config.start_date and config.start_date > date.today():
            message = "Registration has not started yet"
            return flask.render_template('message.html', message=message)

        if config.end_date and config.end_date < date.today():
            message = "Registration has finished"
            return flask.render_template('message.html', message=message)

        return view(*args, **kwargs)

    return wrapper


def add_default_role(user):
    datastore = flask.current_app.extensions['security'].datastore
    default_role = datastore.find_role(DEFAULT_ROLE)
    datastore.add_role_to_user(user, default_role)
    models.db.session.commit()
