from datetime import datetime
import flask
import pytest
from mock import patch
from art17 import models


def _set_config(**kwargs):
    from art17.common import get_config
    from art17.models import db
    for key in kwargs:
        setattr(get_config(), key, kwargs[key])
    db.session.commit()


@pytest.fixture
def zope_auth(app, request):
    from art17.auth import auth

    app.config['AUTH_ZOPE'] = True
    app.config['AUTH_ZOPE_WHOAMI_URL'] = 'http://example.com/'
    app.register_blueprint(auth)

    requests_patch = patch('art17.auth.providers.requests')
    requests = requests_patch.start()
    request.addfinalizer(requests_patch.stop)

    whoami_data = {'user_id': None, 'is_ldap_user': False}
    requests.get.return_value.json.return_value = whoami_data

    return whoami_data


def _create_user(user_id, role_names=[]):
    user = models.RegisteredUser(
        id=user_id,
        account_date=datetime.utcnow(),
        active=True,
    )
    models.db.session.add(user)
    for name in role_names:
        role = models.Role.query.filter_by(name=name).first()
        user.roles.append(role)
    models.db.session.commit()

    return user


def test_identity_is_set_from_zope_whoami(app, zope_auth, client):
    _create_user('ze_admin', ['admin'])

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


def test_self_registration_flow(app, zope_auth, client, outbox):
    from art17.models import RegisteredUser
    from art17.auth.providers import set_user

    _set_config(admin_email='admin@example.com')
    _create_user('ze_admin', ['admin'])

    register_page = client.get(flask.url_for('auth.register'))
    register_page = register_page.click('new art17 consultation account')
    print register_page
    register_page.form['id'] = 'foo'
    register_page.form['email'] = 'foo@example.com'
    register_page.form['password'] = 'p455w4rd'
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
    confirm_page = client.get(url)

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.confirmed_at is not None
    assert not foo_user.active

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "New user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('art17.auth.zope_acl_manager.create') as create_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = True
        activation_page.form.submit()
        assert create_in_zope.call_count == 1

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.active

    assert len(outbox) == 1
    user_message = outbox.pop()
    assert user_message.recipients == ['foo@example.com']
    assert 'has been activated' in user_message.body


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
    _create_user('ze_admin', ['admin'])

    @app.before_request
    def set_testing_user():
        set_user('foo', is_ldap_user=True)

    register_page = client.get(flask.url_for('auth.register_ldap'))
    result_page = register_page.form.submit()
    assert "has been registered" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert not foo_user.active
    assert foo_user.is_ldap

    assert len(outbox) == 1
    admin_message = outbox.pop()
    assert admin_message.recipients == ['admin@example.com']
    assert "Eionet user has registered" in admin_message.body
    url = admin_message.body.split()[-1]
    assert url == 'http://localhost/auth/users/foo'

    with patch('art17.auth.zope_acl_manager.create') as create_in_zope:
        zope_auth['user_id'] = 'ze_admin'
        activation_page = client.get(url)
        activation_page.form['active'] = True
        activation_page.form.submit()
        assert create_in_zope.call_count == 0

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.active

    assert len(outbox) == 1
    user_message = outbox.pop()
    assert user_message.recipients == ['foo@example.com']
    assert 'has been activated' in user_message.body


def test_view_requires_admin(app, zope_auth, client):
    _create_user('ze_admin', ['admin'])
    _create_user('foo')
    admin_user_url = flask.url_for('auth.admin_user', user_id='foo')

    assert client.get(admin_user_url, expect_errors=True).status_code == 403

    zope_auth.update({'user_id': 'ze_admin'})
    assert client.get(admin_user_url).status_code == 200


def test_change_local_password(app, zope_auth, client):
    from flask.ext.security.utils import encrypt_password
    foo = _create_user('foo')
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
    foo = _create_user('foo')
    foo.is_ldap = True
    models.db.session.commit()
    zope_auth.update({'user_id': 'foo', 'is_ldap_user': True})
    page = client.get(flask.url_for('auth.change_password'))
    assert "Please go to the EIONET account change password page" in page
