import os
import hashlib
import base64
from datetime import datetime
from werkzeug.local import LocalProxy
from wtforms import TextField
import flask
from flask.ext.security import SQLAlchemyUserDatastore, AnonymousUser
import flask.ext.security as flask_security
import flask.ext.security.script

from flask.ext.security.forms import (
    ConfirmRegisterForm,
    password_length,
    Required,
)


def ssha(password):
    salt = os.urandom(7)
    if isinstance(password, unicode):
        password = password.encode('utf-8')
    h = hashlib.sha1(password + salt)
    return "{SSHA}" + base64.b64encode(h.digest() + salt)


current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security.core.current_user = current_user
flask_security.views.current_user = current_user
flask_security.views.logout_user = lambda: None
flask_security.views.login_user = lambda new_user: None
flask_security.core._get_login_manager = lambda app: None
flask_security.registerable.encrypt_password = ssha
flask_security.script.encrypt_password = ssha
flask_security.recoverable.encrypt_password = ssha
flask_security.utils.encrypt_password = ssha
flask_security.changeable.encrypt_password = ssha
password_length.min = 1


class UserDatastore(SQLAlchemyUserDatastore):

    def create_user(self, **kwargs):
        kwargs.setdefault('active', False)
        kwargs['account_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, user, role):
        return (self.find_user(id=user), self.find_role(role))


class Art17ConfirmRegisterForm(ConfirmRegisterForm):

    id = TextField('id', validators=[Required("User ID is required")])
