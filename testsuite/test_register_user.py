import flask
from art17 import models


def test_self_registration_flow(app, client, outbox):
    app.config['AUTH_ADMIN_EMAIL'] = 'admin@example.com'

    register_page = client.get(flask.url_for('security.register'))
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


def test_ldap_account_activation_flow(app, client, outbox, ldap_user_info):
    from art17.auth.providers import set_user
    app.config['AUTH_ADMIN_EMAIL'] = 'admin@example.com'
    ldap_user_info['foo'] = {'email': 'foo@example.com'}

    @app.before_request
    def set_testing_user():
        set_user('foo', is_ldap_user=True)

    register_page = client.get(flask.url_for('security.register'))
    result_page = register_page.form.submit().follow()
    assert "Eionet account foo has been activated" in result_page.text

    foo_user = models.RegisteredUser.query.get('foo')
    assert foo_user.email == 'foo@example.com'
    assert foo_user.confirmed_at is not None
    assert not foo_user.active
    assert foo_user.is_ldap
