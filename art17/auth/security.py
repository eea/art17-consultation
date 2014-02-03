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


def get_ldap_user_info(user_id):
    from eea.usersdb import UsersDB
    ldap_server = flask.current_app.config['EEA_LDAP_SERVER']
    users_db = UsersDB(ldap_server=ldap_server)
    return users_db.user_info(user_id)


def register():
    from art17.auth import notify_administrator
    user_credentials = flask.g.get('user_credentials', {})
    if user_credentials.get('is_ldap_user'):
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
            return flask.redirect('/')

        return flask.render_template('auth/register_ldap.html', **{
            'user': flask.g.get('user'),
        })

    return register_orig()

register_orig = flask_security_views.register
flask_security_views.register = register
