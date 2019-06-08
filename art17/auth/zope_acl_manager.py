import requests
import flask


def check_plone_manager(func):
    def inner(*args, **kwargs):
        if not all(_get_config()):
            return
        func(*args, **kwargs)
    return inner


def _get_config():
    app = flask.current_app
    return (
        app.config.get('AUTH_PLONE_ACL_MANAGER_URL'),
        app.config.get('AUTH_PLONE_ACL_MANAGER_KEY'),
    )


@check_plone_manager
def create(user):
    url, key = _get_config()
    resp = requests.post(
        url + '/create_user',
        data={
            'username': user.id,
            'password': user.password,
            'api_key': key,
        },
    )

    if resp.status_code != 200:
        raise RuntimeError("Failed to add user: %s" % resp)


@check_plone_manager
def delete(user):
    url, key = _get_config()
    resp = requests.post(
        url + '/delete_user',
        data={
            'username': user.id,
            'api_key': key,
        },
    )

    if resp.status_code != 200:
        raise RuntimeError("Failed to delete user: %s" % resp)


@check_plone_manager
def edit(user_id, passwd):
    url, key = _get_config()
    resp = requests.post(
        url + '/edit_user',
        data={
            'username': user_id,
            'password': passwd,
            'api_key': key,
        },
    )

    if resp.status_code != 200:
        raise RuntimeError("Failed to edit user: %s" % resp)
