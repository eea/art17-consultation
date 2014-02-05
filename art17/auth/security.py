import os
import hashlib
import base64
from datetime import datetime
from werkzeug.local import LocalProxy
from wtforms import TextField
import flask
from flask.ext.security import SQLAlchemyUserDatastore, AnonymousUser
import flask.ext.security as flask_security

from flask.ext.security.forms import (
    ConfirmRegisterForm,
    password_length,
    Required,
)


current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security.core.current_user = current_user
flask_security.forms.current_user = current_user
flask_security.views.current_user = current_user
flask_security.views.logout_user = lambda: None
flask_security.views.login_user = lambda new_user: None
flask_security.core._get_login_manager = lambda app: None
password_length.min = 1

# zope uses ldap-style SSHA passwords
flask_security.core._allowed_password_hash_schemes[:] = ['ldap_salted_sha1']

# disable hmac, because zope doesn't know about it
flask.ext.security.utils.get_hmac = lambda x: x


class UserDatastore(SQLAlchemyUserDatastore):

    def create_user(self, **kwargs):
        kwargs.setdefault('active', False)
        kwargs['account_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, user, role):
        return (self.find_user(id=user), self.find_role(role))


class Art17ConfirmRegisterForm(ConfirmRegisterForm):

    id = TextField('id', validators=[Required("User ID is required")])
