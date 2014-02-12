import os
import hashlib
import base64
from datetime import datetime
from werkzeug.local import LocalProxy
from wtforms import TextField, ValidationError, SelectField
from wtforms.widgets import HiddenInput
import flask
from flask.ext.security import SQLAlchemyUserDatastore, AnonymousUser
import flask.ext.security.script
import flask.ext.security as flask_security

from flask.ext.security.forms import (
    ConfirmRegisterForm,
    password_length,
    Required,
)

from art17.auth.common import get_ldap_user_info
from art17.models import DicCountryCode, Dataset
from art17.auth.common import check_dates


current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security.core.current_user = current_user
flask_security.forms.current_user = current_user
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
        raise ValidationError("User ID already exists in LDAP database.")


class Art17ConfirmRegisterForm(ConfirmRegisterForm):

    id = TextField('Username', validators=[Required("User ID is required"),
                                     check_duplicate_with_ldap])
    name = TextField('Full name',
        validators=[Required("Full name is required")])
    institution = TextField('Institution',
        validators=[Required("Institution name is required")])
    abbrev = TextField('Institution(abbrev)')
    MS = TextField(widget=HiddenInput(), validators=[Required()])
    country_options = SelectField('MS', validators=[Required()])
    other_country = TextField('Other country')

    def __init__(self, *args, **kwargs):
        super(Art17ConfirmRegisterForm, self).__init__(*args, **kwargs)
        dataset = (Dataset.query.order_by(Dataset.id.desc()).first())
        countries = (DicCountryCode.query
            .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
            .filter(DicCountryCode.dataset_id == dataset.id)
            .distinct()
            .order_by(DicCountryCode.name)
            .all())
        self.country_options.choices = countries + [('', 'Other country')]

    def to_dict(self):
        data = super(Art17ConfirmRegisterForm, self).to_dict()
        data.pop('country_options', None)
        data.pop('other_country', None)
        return data
