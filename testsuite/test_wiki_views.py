import pytest
from urllib import urlencode

from art17.models import db
from .factories import (
    WikiFactory,
    WikiChangeFactory,
    EtcDicBiogeoregFactory,
    WikiTrailFactory,
    WikiTrailChangeFactory,
    WikiCommentFactory,
)
from art17.auth.providers import set_user
from conftest import create_user


@pytest.fixture
def setup(app):
    WikiFactory()
    WikiChangeFactory()
    WikiFactory(
        id=2,
        region_code='',
        habitatcode=1110
    )
    WikiChangeFactory(
        id=2,
        wiki_id=2,
        body='The conservation status in the marine Baltic region',
    )
    EtcDicBiogeoregFactory(
        reg_code='CON',
        reg_name='Continental'
    )
    WikiTrailFactory()
    WikiTrailChangeFactory()
    EtcDicBiogeoregFactory(
        reg_code='MBAL',
        reg_name='Marine Baltic'
    )
    WikiTrailFactory(
        id=2,
        region_code='MBAL',
        habitatcode=1110
    )
    WikiTrailChangeFactory(
        id=2,
        wiki_id=2,
        body='Method 1 was used to evaluate the subconclusion'
    )
    WikiCommentFactory()
    WikiCommentFactory(
        id=2,
        author_id='iulia')
    db.session.commit()


@pytest.mark.parametrize("request_args", [
    (['/species/summary/datasheet/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}]),
    (['/species/summary/audittrail/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}]),
    (['/habitat/summary/datasheet/', {
        'period': '1', 'subject': '9010', 'region': ''}]),
    (['/habitat/summary/audittrail/', {
        'period': '1', 'subject': '9010', 'region': ''}])
])
def test_empty_view(app, client, request_args):
    resp = client.get(*request_args)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert resp.html.find(id='active-wiki').text.strip() == ''


@pytest.mark.parametrize("request_args, search_text", [
    (['/species/summary/datasheet/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}],
        "The wolf was the world's most widely distributed mammal."
     ),
    (['/species/summary/audittrail/', {
        'period': '1', 'subject': 'Canis lupus', 'region': 'CON'}],
        'For Poland: present range, population and habitat'
     ),
    (['/habitat/summary/datasheet/', {
        'period': '1', 'subject': '1110', 'region': ''}],
        'The conservation status in the marine Baltic region'
     ),
    (['/habitat/summary/audittrail/', {
        'period': '1', 'subject': '1110', 'region': 'MBAL'}],
        'Method 1 was used to evaluate the subconclusion'
     )
])
def test_non_auth_view(app, setup, client, request_args, search_text):
    resp = client.get(*request_args)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert resp.html.find(id='active-wiki').text.strip() == search_text


@pytest.mark.parametrize("request_type, request_args, post_params", [
    ('post', ['/species/summary/datasheet/page_history/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}],
        {'revision_id': 1}),
    ('post', ['/species/summary/datasheet/add_comment/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}],
        {'text': 'Test add comment.'}),
    ('post', ['/species/summary/datasheet/edit_page/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}],
        {'text': 'Test edit page.'}),
    ('post', ['/species/summary/datasheet/edit_comment/', {
        'period': '1', 'subject': 'Canis lupus', 'region': '',
        'comment_id': 1}], {'text': 'Test edit comment.'}),
    ('get', ['/species/summary/datasheet/manage_comment/', {
        'comment_id': 1, 'toggle': 'read'}], {}),
    ('get', ['/species/summary/datasheet/get_revision/', {
        'revision_id': 1}], {})
])
def test_perms(app, setup, zope_auth, client, request_type, request_args,
               post_params):
    if request_type == 'post':
        query_string = urlencode(request_args[1])
        final_url = '?'.join((request_args[0], query_string))
        request_args = [final_url, post_params]
    resp = getattr(client, request_type)(*request_args, expect_errors=True)
    assert resp.status_code == 403


@pytest.mark.parametrize("request_args", [
    (['/species/summary/datasheet/manage_comment/', {
        'comment_id': 1, 'toggle': 'del'}]),
    (['/species/summary/datasheet/manage_comment/', {
        'comment_id': 2, 'toggle': 'read'}]),
])
def test_perms_auth_user(app, setup, zope_auth, client, request_args):
    create_user('iulia')
    set_user('iulia')
    resp = client.get(*request_args, expect_errors=True)
    assert resp.status_code == 403


@pytest.mark.parametrize("request_type, request_args, post_params", [
    ('post', ['/species/summary/datasheet/page_history/', {
        'period': '1', 'subject': 'Canis lupus', 'region': ''}],
        {'revision_id': 999}),
    ('post', ['/species/summary/datasheet/edit_comment/', {
        'period': '1', 'subject': 'Canis lupus', 'region': '',
        'comment_id': 999}], {'text': 'Test edit comment.'}),
    ('get', ['/species/summary/datasheet/manage_comment/', {
        'comment_id': 999, 'toggle': 'read'}], {}),
    ('get', ['/species/summary/datasheet/get_revision/', {
        'revision_id': 999}], {})
])
def test_404_error(app, setup, zope_auth, client, request_type, request_args,
                   post_params):
    create_user('iulia')
    set_user('iulia')
    if request_type == 'post':
        query_string = urlencode(request_args[1])
        final_url = '?'.join((request_args[0], query_string))
        request_args = [final_url, post_params]
    resp = getattr(client, request_type)(*request_args, expect_errors=True)
    assert resp.status_code == 404
