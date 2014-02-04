from datetime import datetime
import flask
import pytest
from mock import patch
from art17 import models


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
    app.config['AUTH_ADMIN_EMAIL'] = 'admin@example.com'

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
    assert url == 'http://localhost/auth/admin/foo'
    # TODO login as admin
    activation_page = client.get(url)
    activation_page.form['active'] = True
    activation_page.form.submit()

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.active

    # TODO: user receives email and logs in


def test_ldap_account_activation_flow(app, zope_auth, client, outbox, ldap_user_info):
    from art17.auth.providers import set_user
    app.config['AUTH_ADMIN_EMAIL'] = 'admin@example.com'
    ldap_user_info['foo'] = {'email': 'foo@example.com'}

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
    assert url == 'http://localhost/auth/admin/foo'
