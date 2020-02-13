import flask
import ldap
import os

from datetime import datetime
from collections import defaultdict

from flask import (
    _app_ctx_stack,
    current_app,
    flash,
    g,
    render_template,
    Response,
    redirect,
    request,
    url_for,
)

from flask_principal import PermissionDenied
from flask_login import login_user,login_required, logout_user
from flask_login import current_user as c_user
from flask_security import user_registered
from flask_security.forms import ChangePasswordForm, ResetPasswordForm
from flask_security.changeable import change_user_password
from flask_security.registerable import register_user

from flask_security.utils import verify_password, encrypt_password
from flask_mail import Message

from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from werkzeug.security import generate_password_hash, check_password_hash

from art17 import models
from art17.auth import auth, login_manager, current_user
from art17.auth.common import (
    require_admin,
    set_user_active,
    get_ldap_user_info,
    activate_and_notify_admin,
    add_default_role,
    check_dates,
    safe_send_mail,
)
from art17.auth.forms import DatasetForm, LoginForm
from art17.auth.security import (
    Art17LocalRegisterForm,
    Art17LDAPRegisterForm,
    Art17AdminEditUserForm,
    AnonymousUser,
    encrypt_password,
    verify
)
from art17.common import HOMEPAGE_VIEW_NAME, get_config


def user_registered_sighandler(app, user, confirm_token):
    add_default_role(user)


user_registered.connect(user_registered_sighandler)


@auth.app_errorhandler(PermissionDenied)
def handle_permission_denied(error):
    html = render_template('auth/permission_denied.html')
    return Response(html, status=403)


@auth.route('/auth/register/local', methods=['GET', 'POST'])
def register_local():
    form = Art17LocalRegisterForm(request.form)

    if form.validate_on_submit():
        register_user(**form.to_dict())
        return render_template('message.html', message="")

    return render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


def send_welcome_email(user, plaintext_password=None):
    app = current_app
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = render_template('auth/email_user_welcome.txt', **{
        'user': user,
        'plaintext_password': plaintext_password,
        'home_url': url_for(HOMEPAGE_VIEW_NAME, _external=True),
    })
    safe_send_mail(app, msg)


@auth.route('/auth/create_local', methods=['GET', 'POST'])
@require_admin
def admin_create_local():
    form = Art17LocalRegisterForm(request.form)

    if form.validate_on_submit():
        kwargs = form.to_dict()
        plaintext_password = kwargs['password']
        encrypted_password = encrypt_password(plaintext_password)
        datastore = current_app.extensions['security'].datastore
        user = datastore.create_user(**kwargs)
        user.confirmed_at = datetime.utcnow()
        set_user_active(user, True)
        user.password = encrypted_password
        datastore.commit()
        send_welcome_email(user, plaintext_password)
        flash("User %s created successfully." % kwargs['id'], 'success')
        return redirect(url_for('.users'))

    return render_template('auth/register_local.html', **{
        'register_user_form': form,
    })


def _get_initial_ldap_data(user_id):
    ldap_user_info = get_ldap_user_info(user_id)
    if ldap_user_info is None:
        return None
    return {
        'name': ldap_user_info.get('full_name'),
        'institution': ldap_user_info.get('organisation'),
        'qualification': ldap_user_info.get('job_title'),
        'email': ldap_user_info.get('email'),
    }


@auth.route('/auth/register/ldap', methods=['GET', 'POST'])
@check_dates
def register_ldap():
    #TODO maybe remove as the user is now registered on first LDAP login
    user_credentials = g.get('user_credentials', {})
    user_id = user_credentials.get('user_id')

    if not user_credentials.get('is_ldap_user'):
        if user_id:
            message = "You are already logged in."
            return render_template('message.html', message=message)

        else:
            message = (
                'First log into your EIONET account by clicking "login" '
                'at the top of the page.'
            )
            return render_template('message.html', message=message)

    if user_id and g.identity.id:
        return render_template('auth/register_ldap_exists.html', **{
            'admin_email': get_config().admin_email,
        })
    initial_data = _get_initial_ldap_data(user_id)
    form = Art17LDAPRegisterForm(ImmutableMultiDict(initial_data))

    if request.method == 'POST':
        form = Art17LDAPRegisterForm(request.form)
        form.name.data = initial_data.get('name', '')
        form.email.data = initial_data.get('email', '')
        if form.validate():
            datastore = current_app.extensions['security'].datastore
            user = datastore.create_user(
                id=user_id,
                is_ldap=True,
                password='',
                confirmed_at=datetime.utcnow(),
                **form.to_dict()
            )
            datastore.commit()
            flash(
                "Eionet account %s has been activated"
                % user_id,
                'success',
            )
            activate_and_notify_admin(_app_ctx_stack.top.app, user)
            add_default_role(user)
            return render_template('auth/register_ldap_done.html')

    return render_template('auth/register_ldap.html', **{
        'already_registered': g.get('user') is not None,
        'user_id': user_id,
        'register_user_form': form,
    })


@auth.route('/auth/create_ldap', methods=['GET', 'POST'])
@require_admin
def admin_create_ldap():
    user_id = request.form.get('user_id')
    if user_id is None:
        return render_template('auth/register_ldap_enter_user_id.html')

    if models.RegisteredUser.query.get(user_id) is not None:
        flash('User "%s" already registered.' % user_id, 'error')
        return redirect(url_for('.admin_create_ldap'))

    initial_data = _get_initial_ldap_data(user_id)
    if '_fields_from_ldap' in request.form:
        if initial_data is None:
            flash('User "%s" not found in Eionet.' % user_id, 'error')
            return redirect(url_for('.admin_create_ldap'))
        form = Art17LDAPRegisterForm(ImmutableMultiDict(initial_data))
    else:
        form = Art17LDAPRegisterForm(request.form)
        form.name.data = initial_data.get('name', '')
        form.email.data = initial_data.get('email', '') or form.email.data
        if form.validate():
            kwargs = form.to_dict()
            kwargs['id'] = user_id
            kwargs['is_ldap'] = True
            datastore = current_app.extensions['security'].datastore
            user = datastore.create_user(**kwargs)
            user.confirmed_at = datetime.utcnow()
            set_user_active(user, True)
            datastore.commit()
            send_welcome_email(user)
            flash(
                "User %s created successfully." % kwargs['id'],
                'success',
            )
            return redirect(url_for('.users'))

    return render_template('auth/register_ldap.html', **{
        'user_id': user_id,
        'register_user_form': form,
    })


@auth.route('/auth/me')
def me():
    return render_template('auth/me.html')


@auth.route('/auth/change_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_anonymous:
        message = "You must log in before changing your password."
        return render_template('message.html', message=message)

    if current_user.is_ldap:
        message = (
            'Your password can be changed only from the EIONET website '
            + '('
            + os.environ.get('EEA_PASSWORD_RESET')
            + ').'
        )
        return render_template('message.html', message=message)

    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_user.password = encrypt_password(form.new_password.data)
        models.db.session.commit()
        models.db.session.commit()
        msg = "Your password has been changed. Please log in again."
        flash(msg, 'success')
        return redirect(url_for(HOMEPAGE_VIEW_NAME))

    return render_template('auth/change_password.html', **{
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
    app = current_app
    role_description = {row.name: row.description for row in models.Role.query}
    msg = Message(
        subject="Role update on the Biological Diversity website",
        sender=app.extensions['security'].email_sender,
        recipients=[user.email],
    )
    msg.body = render_template('auth/email_user_role_change.txt', **{
        'user': user,
        'new_roles': [role_description[r] for r in new_roles],
    })
    safe_send_mail(app, msg)


@auth.route('/auth/users')
@require_admin
def users():
    user_query = models.RegisteredUser.query.order_by(models.RegisteredUser.id)
    dataset = (models.Dataset.query.order_by(models.Dataset.id.desc()).first())
    countries = (
        models.DicCountryCode.query
        .with_entities(
            models.DicCountryCode.codeEU,
            models.DicCountryCode.name
        )
        .filter(models.DicCountryCode.dataset_id == dataset.id)
        .distinct()
        .order_by(models.DicCountryCode.name)
        .all()
    )
    return render_template('auth/users.html', **{
        'user_list': user_query.all(),
        'role_map': get_roles_for_all_users(),
        'countries': dict(countries),
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

    if request.method == 'POST':
        if request.form.get('btn') == u'delete':
            # delete from local database
            user = models.RegisteredUser.query.get(user_id)
            models.db.session.delete(user)
            models.db.session.commit()
            flash("User %s has successfully been deleted" % user_id, 'success')
            return redirect(url_for('.users'))
        else:
            user_form = Art17AdminEditUserForm(request.form, obj=user)
            if user_form.validate():
                # manage status
                set_user_active(user, user_form.active.data)

                # manage roles
                datastore = current_app.extensions['security'].datastore
                new_roles = request.form.getlist('roles')
                expandable_roles = filter(lambda k: k not in new_roles, current_user_roles)
                for role in new_roles:
                    datastore.add_role_to_user(user_id, role)
                for role in expandable_roles:
                    datastore.remove_role_from_user(user_id, role)
                datastore.commit()

                # manage user info
                user_form.populate_obj(user)
                models.db.session.commit()

                # manage role notifications
                if request.form.get('notify_user', type=bool):
                    send_role_change_notification(user, new_roles)

                flash("User information updated for %s" % user_id, 'success')
                return redirect(url_for('.users'))
    else:
        user_form = Art17AdminEditUserForm(obj=user)

    return render_template('auth/admin_user.html', **{
        'user': user,
        'user_form': user_form,
        'current_user_roles': current_user_roles,
        'all_roles': dict(all_roles),
    })


@auth.route('/auth/users/<user_id>/reset_password', methods=['GET', 'POST'])
@require_admin
def admin_user_reset_password(user_id):
    user = models.RegisteredUser.query.get_or_404(user_id)
    if user.is_ldap:
        message = (
            'The password can be changed only from the EIONET website '
            + '('
            + os.environ.get('EEA_PASSWORD_RESET')
            + ').'
        )
        return render_template('message.html', message=message)

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.password = encrypt_password(form.password.data)
        models.db.session.commit()
        msg = "Password successfully reseted."
        flash(msg, 'success')
    return render_template('auth/admin_user_reset_password.html', **{
        'user': user,
        'form': form,
    })


@auth.route('/admin/dataset/')
@require_admin
def dataset_list():
    ds = models.Dataset.query.all()
    return render_template('admin/dataset_list.html', datasets=ds)


@auth.route('/admin/dataset/<dataset_id>', methods=['GET', 'POST'])
@require_admin
def dataset_edit(dataset_id):
    dataset = models.Dataset.query.get_or_404(dataset_id)

    if request.method == 'POST':
        form = DatasetForm(request.form)
        if form.validate():
            form.populate_obj(dataset)
            models.db.session.commit()
            flash("Dataset updated")
            return redirect(url_for('.dataset_list'))
    else:
        form = DatasetForm(obj=dataset)
    return render_template('admin/dataset_edit.html',
                           dataset=dataset, form=form)

@login_manager.user_loader
def load_user(id=None):
    return models.RegisteredUser.query.get(id)

@auth.before_request
def get_current_user():
    g.user = AnonymousUser() if not hasattr(c_user, "id")  else c_user

def try_local_login(username, password, form):
    user = models.RegisteredUser.query.filter_by(id=username).first()
    if not user or not verify(password, user):
        flash('Please check your login details and try again.')
        return render_template('login.html', form=form)
    login_user(user)
    g.user = user
    flash('You have successfully logged in.', 'success')
    return redirect(url_for(HOMEPAGE_VIEW_NAME))


@auth.route('/auth/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for(HOMEPAGE_VIEW_NAME))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            models.RegisteredUser.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:

            try_local_login(username, password, form)
            if not current_user.is_authenticated:
                flash(
                    'Invalid username or password. Please try again.',
                    'danger')
                return render_template('login.html', form=form)

        user = models.RegisteredUser.query.filter_by(id=username).first()

        if not user:
            data = _get_initial_ldap_data(username)
            user = models.RegisteredUser(
                id=username,
                name=data['name'],
                qualification=data['qualification'],
                email=data['email'],
                institution=data['institution'],
                password=encrypt_password(password),
                is_ldap=True,
                account_date=datetime.now()
            )
            models.db.session.add(user)
            models.db.session.commit()
        login_user(user)
        g.user = user
        flash('You have successfully logged in.', 'success')
        return redirect(url_for(HOMEPAGE_VIEW_NAME))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form)

@auth.route('/auth/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for(HOMEPAGE_VIEW_NAME))
