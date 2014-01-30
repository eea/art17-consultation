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
