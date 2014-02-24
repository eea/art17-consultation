import inspect
import flask
import flask.ext.security.script
import flask.ext.security as flask_security
from flask.ext.security import SQLAlchemyUserDatastore, AnonymousUser
from flask_wtf import Form
from datetime import datetime
from werkzeug.local import LocalProxy
from wtforms import TextField, BooleanField, ValidationError, Field

from flask.ext.security.forms import (
    ConfirmRegisterForm,
    RegisterFormMixin,
    ForgotPasswordForm,
    password_length,
    Required,
    email_validator,
    unique_user_email,
)

from art17.auth.common import get_ldap_user_info
from art17.auth.common import check_dates
from art17.auth.forms import Art17RegisterFormBase, CustomEmailTextField
from art17 import models


current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security.core.current_user = current_user
flask_security.forms.current_user = current_user
flask_security.decorators.current_user = current_user
flask_security.views.current_user = current_user
flask_security.views.logout_user = lambda: None
flask_security.views.login_user = lambda new_user: None
flask_security.views.register = check_dates(flask_security.views.register)
flask_security.core._get_login_manager = lambda app: None
password_length.min = 1

# zope uses ldap-style SSHA passwords
flask_security.core._allowed_password_hash_schemes[:] = ['ldap_salted_sha1']


def encrypt_password(password):
    pwd_context = flask.current_app.extensions['security'].pwd_context
    return pwd_context.encrypt(password.encode('utf-8'))


def verify(password, user):
    pwd_context = flask.current_app.extensions['security'].pwd_context
    return pwd_context.verify(password, user.password)


# override encrypt_password with our simplified version
flask_security.registerable.encrypt_password = encrypt_password
flask_security.script.encrypt_password = encrypt_password
flask_security.recoverable.encrypt_password = encrypt_password
flask_security.utils.encrypt_password = encrypt_password
flask_security.changeable.encrypt_password = encrypt_password
flask_security.forms.verify_and_update_password = verify


class UserDatastore(SQLAlchemyUserDatastore):

    def create_user(self, **kwargs):
        kwargs.setdefault('active', False)
        kwargs['account_date'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, user, role):
        return (self.find_user(id=user), self.find_role(role))


def check_duplicate_with_ldap(form, field):

    user = get_ldap_user_info(field.data)
    if user is not None:
        raise ValidationError("Username already exists in the EIONET database.")


def check_duplicate_with_local_db(form, field):

    user = models.RegisteredUser.query.get(field.data)
    if user is not None:
        raise ValidationError("Username already exists")


def custom_unique_user_email(form, field):
    obj = getattr(form, 'obj', None)
    datastore = flask.current_app.extensions['security'].datastore
    check = datastore.find_user(email=field.data)

    # check for editing existing objects
    if check and getattr(obj, 'id', None) != check.id:
        raise ValidationError("%s is already associated with an account" %
                                field.data)


class Art17LocalRegisterForm(Art17RegisterFormBase, ConfirmRegisterForm):

    id = TextField('Username',
        validators=[Required("User ID is required"),
                    check_duplicate_with_local_db,
                    check_duplicate_with_ldap])

    email = CustomEmailTextField('Email address',
        validators=[Required("Email is required"),
                    email_validator,
                    unique_user_email])


class Art17LDAPRegisterForm(Art17RegisterFormBase, RegisterFormMixin, Form):

    email = TextField('Email address',
        validators=[Required("Email is required"),
                    email_validator])


class Art17AdminEditUserForm(Art17RegisterFormBase, Form):

    active = BooleanField('Active',
                          description='*(allow user to login and gain roles)')
    email = TextField('Email address',
                      validators=[Required("Email is required"),
                                  email_validator,
                                  custom_unique_user_email])


def no_ldap_user(form, field):
    if form.user is not None:
        if form.user.is_ldap:
            raise ValidationError("Please use the password recovery "
                                  "system for Eionet accounts")


class Art17ForgotPasswordForm(ForgotPasswordForm):

    email = TextField(
        label=ForgotPasswordForm.email.args[0],
        validators=ForgotPasswordForm.email.kwargs['validators']
                   + [no_ldap_user],
    )
