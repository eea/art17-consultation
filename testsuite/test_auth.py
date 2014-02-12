import flask
from mock import patch

from art17 import models
from conftest import create_user


def _set_config(**kwargs):
    from art17.common import get_config
    from art17.models import db
    for key in kwargs:
        setattr(get_config(), key, kwargs[key])
    db.session.commit()


def test_identity_is_set_from_zope_whoami(app, zope_auth, client):
    create_user('ze_admin', ['admin'])

    @app.route('/identity')
    def get_identity():
        identity = flask.g.identity
        return flask.jsonify(
            id=identity.id,
            provides=sorted(list(identity.provides)),
        )

    zope_auth.update({'user_id': 'ze_admin', 'is_ldap_user': False})

    identity = client.get('/identity').json
    assert identity['id'] == 'ze_admin'
    assert identity['provides'] == [['id', 'ze_admin'], ['role', 'admin']]


def test_self_registration_flow(app, zope_auth, client, outbox, ldap_user_info):
    from art17.models import RegisteredUser
    from art17.auth.providers import set_user
    from .factories import DatasetFactory

    _set_config(admin_email='admin@example.com')
    create_user('ze_admin', ['admin'])
    DatasetFactory()
    models.db.session.commit()

    register_page = client.get(flask.url_for('auth.register_local'))
    register_page.form['id'] = 'foo'
    register_page.form['email'] = 'foo@example.com'
    register_page.form['password'] = 'p455w4rd'
    register_page.form['name'] = 'foo me'
    register_page.form['institution'] = 'foo institution'
    result_page = register_page.form.submit().follow()
    assert "Confirmation instructions have been sent" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is None
    assert not foo_user.active
    assert not foo_user.is_ldap
    assert foo_user.password.startswith('{SSHA}')

    assert len(outbox) == 1
    confirm_message = outbox.pop()
    assert 'Welcome foo@example.com!' in confirm_message.body
    url = confirm_message.body.split()[-1]
    assert url.startswith("http://localhost/confirm/")

    with patch('art17.auth.zope_acl_manager.create') as create_in_zope:
        client.get(url)
        assert create_in_zope.call_count == 1

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.confirmed_at is not None
    assert foo_user.active

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "New user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('art17.auth.zope_acl_manager.delete') as delete_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = False
        activation_page.form.submit()
        assert delete_in_zope.call_count == 1

    foo_user = models.RegisteredUser.query.get('foo')
    assert not foo_user.active


def test_ldap_account_activation_flow(
        app,
        zope_auth,
        client,
        outbox,
        ldap_user_info,
):
    from art17.auth.providers import set_user
    _set_config(admin_email='admin@example.com')
    ldap_user_info['foo'] = {'email': 'foo@example.com'}
    create_user('ze_admin', ['admin'])

    @app.before_request
    def set_testing_user():
        set_user('foo', is_ldap_user=True)

    register_page = client.get(flask.url_for('auth.register_ldap'))

    with patch('art17.auth.zope_acl_manager.create') as create_in_zope:
        result_page = register_page.form.submit()
        assert create_in_zope.call_count == 0

    assert "has been registered" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "Eionet user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('art17.auth.zope_acl_manager.delete') as delete_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = False
        activation_page.form.submit()
        assert delete_in_zope.call_count == 0

    foo_user = models.RegisteredUser.query.get('foo')
    assert not foo_user.active


def test_view_requires_admin(app, zope_auth, client):
    create_user('ze_admin', ['admin'])
    create_user('foo')
    admin_user_url = flask.url_for('auth.admin_user', user_id='foo')

    assert client.get(admin_user_url, expect_errors=True).status_code == 403

    zope_auth.update({'user_id': 'ze_admin'})
    assert client.get(admin_user_url).status_code == 200


def test_change_local_password(app, zope_auth, client):
    from flask.ext.security.utils import encrypt_password
    foo = create_user('foo')
    old_enc_password = encrypt_password('my old pw')
    foo.password = old_enc_password
    models.db.session.commit()

    zope_auth.update({'user_id': 'foo'})
    page = client.get(flask.url_for('auth.change_password'))
    page.form['password'] = 'my old pw'
    page.form['new_password'] = 'the new pw'
    page.form['new_password_confirm'] = 'the new pw'
    with patch('art17.auth.zope_acl_manager.create') as create_in_zope:
        confirmation_page = page.form.submit().follow()

    assert "password has been changed" in confirmation_page.text
    assert create_in_zope.call_count == 1

    foo = models.RegisteredUser.query.filter_by(id='foo').first()
    assert foo.password != old_enc_password


def test_change_anonymous_password(app, zope_auth, client):
    page = client.get(flask.url_for('auth.change_password'))
    assert "You must log in before changing your password" in page


def test_change_ldap_password(app, zope_auth, client):
    foo = create_user('foo')
    foo.is_ldap = True
    models.db.session.commit()
    zope_auth.update({'user_id': 'foo', 'is_ldap_user': True})
    page = client.get(flask.url_for('auth.change_password'))
    assert "Please go to the EIONET account change password page" in page


def test_dates(app, zope_auth, client):
    from datetime import date, timedelta

    today = date.today()

    _set_config(
        start_date=today + timedelta(days=2),
        end_date=today + timedelta(days=4),
    )
    page = client.get(flask.url_for('auth.register_ldap'))
    assert "Registration has not started yet" in page

    _set_config(
        start_date=today - timedelta(days=4),
        end_date=today - timedelta(days=2),
    )
    page = client.get(flask.url_for('auth.register_ldap'))
    assert "Registration has finished" in page
