from datetime import datetime

import flask
import flask_security as flask_security
import flask_security.utils
from flask_login import current_user as c_user
from flask_security.core import AnonymousUser as BaseAnonymousUser
from flask_security import SQLAlchemyUserDatastore
from flask_security.forms import ConfirmRegisterForm  # password_length,
from flask_security.forms import (
    ForgotPasswordForm,
    RegisterFormMixin,
    Required,
    unique_user_email,
)
from flask_wtf import FlaskForm
from werkzeug.local import LocalProxy
from wtforms import BooleanField, StringField, ValidationError
from wtforms.validators import Email
from art17.auth.common import check_dates, get_ldap_user_info
from art17.auth.forms import Art17RegisterFormBase, CustomEmailStringField
from art17.models import RegisteredUser


class AnonymousUser(BaseAnonymousUser):
    id = None


current_user = LocalProxy(
    lambda: AnonymousUser() if not c_user.is_authenticated else c_user
)
flask_security.core.current_user = current_user
flask_security.core.AnonymousUser = AnonymousUser
flask_security.forms.current_user = current_user
flask_security.decorators.current_user = current_user
flask_security.views.current_user = current_user
flask_security.views.logout_user = lambda: None
flask_security.views.login_user = lambda new_user, authn_via: None
flask_security.views.register = check_dates(flask_security.views.register)
# password_length.min = 1

# ldap uses ldap-style SSHA passwords
# flask_security.core._allowed_password_hash_schemes = ['ldap_salted_sha1']


def encrypt_password(password):
    pwd_context = flask.current_app.extensions["security"].pwd_context
    return pwd_context.hash(password.encode("utf-8"))


def verify(password, user):
    pwd_context = flask.current_app.extensions["security"].pwd_context
    return pwd_context.verify(password, user.password)


# override encrypt_password with our simplified version
flask_security.registerable.encrypt_password = encrypt_password
flask_security.utils.encrypt_password = encrypt_password
flask_security.recoverable.encrypt_password = encrypt_password
flask_security.utils.encrypt_password = encrypt_password
flask_security.changeable.encrypt_password = encrypt_password
flask_security.forms.verify_and_update_password = verify


class UserDatastore(SQLAlchemyUserDatastore):
    def create_user(self, **kwargs):
        kwargs.setdefault("active", False)
        kwargs["account_date"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        return super(UserDatastore, self).create_user(**kwargs)

    def _prepare_role_modify_args(self, role):
        if isinstance(role, str):
            role = self.find_role(role)
        return role


def check_duplicate_with_ldap(form, field):

    user = get_ldap_user_info(field.data)
    if user is not None:
        raise ValidationError("Username already exists in the EIONET database.")


def check_duplicate_with_local_db(form, field):

    user = RegisteredUser.query.get(field.data)
    if user is not None:
        raise ValidationError("Username already exists")


def custom_unique_user_email(form, field):
    obj = getattr(form, "obj", None)
    datastore = flask.current_app.extensions["security"].datastore
    check = datastore.find_user(email=field.data)

    # check for editing existing objects
    if check and getattr(obj, "id", None) != check.id:
        raise ValidationError("%s is already associated with an account" % field.data)


class Art17LocalRegisterForm(Art17RegisterFormBase, ConfirmRegisterForm):

    id = StringField(
        "Username",
        validators=[
            Required("User ID is required"),
            check_duplicate_with_local_db,
            check_duplicate_with_ldap,
        ],
    )

    email = CustomEmailStringField(
        "Email address",
        validators=[
            Required("Email is required"),
            Email("Invalid email address"),
            unique_user_email,
        ],
    )


class Art17LDAPRegisterForm(Art17RegisterFormBase, RegisterFormMixin, FlaskForm):

    email = StringField(
        "Email address",
        validators=[Required("Email is required"), Email("Invalid email address")],
    )


class Art17AdminEditUserForm(Art17RegisterFormBase, FlaskForm):

    active = BooleanField(
        "Active", description="User is allowed to login and gain roles."
    )
    email = StringField(
        "Email address",
        validators=[
            Required("Email is required"),
            Email("Invalid email address"),
            custom_unique_user_email,
        ],
    )


def no_ldap_user(form, field):
    if form.user is not None:
        if form.user.is_ldap:
            raise ValidationError(
                "Please use the password recovery " "system for Eionet accounts"
            )


class Art17ForgotPasswordForm(ForgotPasswordForm):

    email = StringField(
        label=ForgotPasswordForm.email.args[0],
        validators=ForgotPasswordForm.email.kwargs["validators"] + [no_ldap_user],
    )
