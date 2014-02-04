from datetime import datetime
from werkzeug.local import LocalProxy
from wtforms import TextField
import flask
from flask.ext.security import SQLAlchemyUserDatastore, AnonymousUser
from flask.ext.security import core as flask_security_core
from flask.ext.security import views as flask_security_views
from flask.ext.security.forms import (
    ConfirmRegisterForm,
    password_length,
    Required,
)

current_user = LocalProxy(lambda: flask.g.get('user') or AnonymousUser())
flask_security_core.current_user = current_user
flask_security_views.current_user = current_user
flask_security_views.logout_user = lambda: None
flask_security_views.login_user = lambda new_user: None
flask_security_core._get_login_manager = lambda app: None
password_length.min = 1


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
