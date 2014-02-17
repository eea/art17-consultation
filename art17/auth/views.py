from datetime import datetime
from collections import defaultdict
import flask
from flask.ext.principal import PermissionDenied
from flask.ext.security.forms import ChangePasswordForm
from flask.ext.security.changeable import change_user_password
from flask.ext.security.registerable import register_user, encrypt_password
from flask.ext.mail import Message
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from art17 import models
from art17.auth.forms import DatasetForm
from art17.common import HOMEPAGE_VIEW_NAME, get_config
from art17.auth import zope_acl_manager, current_user, auth
from art17.auth.security import (
    Art17LocalRegisterForm,
    Art17LDAPRegisterForm,
)
from art17.auth.common import (
    require_admin,
    set_user_active,
    get_ldap_user_info,
    activate_and_notify_admin,
    check_dates,
    alter_user_info,
    COMMON_USER_INFO_FIELDS,
)


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = flask.render_template('auth/permission_denied.html')
    return flask.Response(html, status=403)


@auth.route('/auth/register/local', methods=['GET', 'POST'])
def register_local():
    form = Art17LocalRegisterForm(flask.request.form)

    if form.validate_on_submit():
        register_user(**form.to_dict())
        return flask.render_template('message.html', message="")

    return flask.render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


def send_welcome_email(user, plaintext_password=None):
    app = flask.current_app
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = flask.render_template('auth/email_user_welcome.txt', **{
        'user': user,
        'plaintext_password': plaintext_password,
        'home_url': flask.url_for(HOMEPAGE_VIEW_NAME, _external=True),
    })
    app.extensions['mail'].send(msg)


@auth.route('/auth/create_local', methods=['GET', 'POST'])
def admin_create_local():
    form = Art17LocalRegisterForm(flask.request.form)

    if form.validate_on_submit():
        kwargs = form.to_dict()
        plaintext_password = kwargs['password']
        kwargs['password'] = encrypt_password(plaintext_password)
        datastore = flask.current_app.extensions['security'].datastore
        user = datastore.create_user(**kwargs)
        user.confirmed_at = datetime.utcnow()
        set_user_active(user, True)
        datastore.commit()
        send_welcome_email(user, plaintext_password)
        flask.flash("User %s created successfully." % kwargs['id'], 'success')
        return flask.redirect(flask.url_for('.admin_create_local'))

    return flask.render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


def _get_initial_ldap_data(user_id):
    ldap_user_info = get_ldap_user_info(user_id)
    return {
        'name': ldap_user_info.get('full_name'),
        'institution': ldap_user_info.get('organisation'),
        'qualification': ldap_user_info.get('job_title'),
        'email': ldap_user_info.get('email'),
    }


@auth.route('/auth/register/ldap', methods=['GET', 'POST'])
@check_dates
def register_ldap():
    user_credentials = flask.g.get('user_credentials', {})
    user_id = user_credentials.get('user_id')

    if not user_credentials.get('is_ldap_user'):
        if user_id:
            message = "You are already logged in."
            return flask.render_template('message.html', message=message)

        else:
            message = (
                'First log into your EIONET account by clicking "login" '
                'at the top of the page.'
            )
            return flask.render_template('message.html', message=message)

    if user_id and flask.g.identity.id:
        return flask.render_template('auth/register_ldap_exists.html', **{
            'admin_email': get_config().admin_email,
        })

    initial_data = _get_initial_ldap_data(user_id)
    form = Art17LDAPRegisterForm(ImmutableMultiDict(initial_data))

    if flask.request.method == 'POST':
        form = Art17LDAPRegisterForm(flask.request.form)
        if form.validate():
            datastore = flask.current_app.extensions['security'].datastore
            user = datastore.create_user(
                id=user_id,
                is_ldap=True,
                password='',
                confirmed_at=datetime.utcnow(),
                **form.to_dict()
            )
            datastore.commit()
            flask.flash(
                "Eionet account %s has been activated"
                % user_id,
                'success',
            )
            activate_and_notify_admin(flask._app_ctx_stack.top.app, user)
            return flask.render_template('auth/register_ldap_done.html')

    return flask.render_template('auth/register_ldap.html', **{
        'already_registered': flask.g.get('user') is not None,
        'user_id': user_id,
        'register_user_form': form,
    })


@auth.route('/auth/create_ldap', methods=['GET', 'POST'])
def admin_create_ldap():
    user_id = flask.request.args.get('user_id')
    if user_id is None:
        return flask.render_template('auth/register_ldap_enter_user_id.html')

    if flask.request.method == 'GET':
        initial_data = _get_initial_ldap_data(user_id)
        form = Art17LDAPRegisterForm(ImmutableMultiDict(initial_data))

    else:
        form = Art17LDAPRegisterForm(flask.request.form)
        if form.validate():
            kwargs = form.to_dict()
            kwargs['id'] = user_id
            kwargs['is_ldap'] = True
            datastore = flask.current_app.extensions['security'].datastore
            user = datastore.create_user(**kwargs)
            user.confirmed_at = datetime.utcnow()
            set_user_active(user, True)
            datastore.commit()
            send_welcome_email(user)
            flask.flash(
                "User %s created successfully." % kwargs['id'],
                'success',
            )
            return flask.redirect(flask.url_for('.admin_create_ldap'))

    return flask.render_template('auth/register_ldap.html', **{
        'register_user_form': form,
    })


@auth.route('/auth/me')
def me():
    return flask.render_template('auth/me.html')


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


def get_roles_for_all_users():
    roles_query = (
        models.db.session.query(
            models.roles_users.c.registered_users_user,
            models.Role.name,
        )
        .join(
            models.Role,
            models.roles_users.c.role_id == models.Role.id,
        )
    )

    rv = defaultdict(list)
    for user_id, role_name in roles_query:
        rv[user_id].append(role_name)
    return dict(rv)


def send_role_change_notification(user, new_roles):
    app = flask.current_app
    role_description = {row.name: row.description for row in models.Role.query}
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = flask.render_template('auth/email_user_role_change.txt', **{
        'user': user,
        'new_roles': [role_description[r] for r in new_roles],
    })
    app.extensions['mail'].send(msg)


@auth.route('/auth/users')
@require_admin
def users():
    user_query = models.RegisteredUser.query.order_by(models.RegisteredUser.id)
    return flask.render_template('auth/users.html', **{
        'user_list': user_query.all(),
        'role_map': get_roles_for_all_users(),
    })


@auth.route('/auth/users/<user_id>', methods=['GET', 'POST'])
@require_admin
def admin_user(user_id):
    user = models.RegisteredUser.query.get_or_404(user_id)
    current_user_roles = [r.name for r in user.roles]
    all_roles = (
        models.Role.query
        .with_entities(models.Role.name, models.Role.description)
        .order_by(models.Role.id)
        .all()
    )

    # we use LDAP reg form as it is the closest to what an admin should edit
    user_form = Art17LDAPRegisterForm(
        ImmutableMultiDict([(field, getattr(user, field))
            for field in COMMON_USER_INFO_FIELDS])
    )

    if flask.request.method == 'POST':
        # manage status
        set_user_active(user, flask.request.form.get('active', type=bool))

        # manage roles
        datastore = flask.current_app.extensions['security'].datastore
        new_roles = flask.request.form.getlist('roles')
        expandable_roles = filter(lambda k: k not in new_roles, current_user_roles)
        for role in new_roles:
            datastore.add_role_to_user(user_id, role)
        for role in expandable_roles:
            datastore.remove_role_from_user(user_id, role)
        datastore.commit()

        # manage user info
        alter_user_info(user, **flask.request.form.to_dict())

        if flask.request.form.get('notify_user', type=bool):
            send_role_change_notification(user, new_roles)

        flask.flash("User information updated for %s" % user_id, 'success')
        return flask.redirect(flask.url_for('.users', user_id=user_id))

    return flask.render_template('auth/admin_user.html', **{
        'user': user,
        'user_form': user_form,
        'current_user_roles': current_user_roles,
        'all_roles': dict(all_roles),
    })


@auth.route('/admin/dataset/')
@require_admin
def dataset_list():
    ds = models.Dataset.query.all()
    return flask.render_template('admin/dataset_list.html', datasets=ds)


@auth.route('/admin/dataset/<dataset_id>', methods=['GET', 'POST'])
@require_admin
def dataset_edit(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    if flask.request.method == 'POST':
        form = DatasetForm(flask.request.form)
        if form.validate():
            form.populate_obj(dataset)
            models.db.session.commit()
            flask.flash("Dataset updated")
            return flask.redirect(flask.url_for('.dataset_list'))
    else:
        form = DatasetForm(obj=dataset)
    return flask.render_template('admin/dataset_edit.html',
                                 dataset=dataset, form=form)
