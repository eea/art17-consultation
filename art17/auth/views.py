from datetime import datetime
import flask
from flask.ext.principal import PermissionDenied
from flask.ext.security.forms import ChangePasswordForm
from flask.ext.security.changeable import change_user_password
from art17 import models
from art17.common import HOMEPAGE_VIEW_NAME
from art17.auth import zope_acl_manager, current_user, auth
from art17.auth.common import (
    require_admin,
    set_user_active,
    get_ldap_user_info,
    put_in_activation_queue,
)


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = flask.render_template('auth/permission_denied.html')
    return flask.Response(html, status=403)


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
