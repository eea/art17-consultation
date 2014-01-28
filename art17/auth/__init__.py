import flask
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


@security_signals.user_confirmed.connect
def notify_administrator(app, user, **extra):
    msg = Message(
        subject="User has registered",
        sender=app.extensions['security'].email_sender,
        recipients=[app.config['AUTH_ADMIN_EMAIL']],
    )
    msg.body = flask.render_template(
        'auth/email_activate_user.txt',
        activation_link=flask.url_for(
            'auth.admin_user',
            user_id=user.id,
            _external=True,
        ),
    )
    app.extensions['mail'].send(msg)

auth = flask.Blueprint('auth', __name__)
security = Security(
    datastore=UserDatastore(
        models.db,
        models.RegisteredUser,
        models.Role,
    ),
)


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
    })

    security.init_app(
        app,
        confirm_register_form=Art17ConfirmRegisterForm,
    )


@auth.route('/auth/admin/<user_id>', methods=['GET', 'POST'])
def admin_user(user_id):
    user = models.RegisteredUser.query.get_or_404(user_id)
    if flask.request.method == 'POST':
        user.active = flask.request.form.get('active', type=bool)
        models.db.session.commit()
        flask.flash("User information updated for %s" % user_id, 'success')
        return flask.redirect(flask.url_for('.admin_user', user_id=user_id))

    return flask.render_template('auth/admin_user.html', user=user)
