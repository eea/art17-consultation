import pytest

from . import factories
from art17 import models
from conftest import create_user


@pytest.fixture
def setup_common(app):
    factories.EtcDataSpeciesRegionFactory(
        assesment_speciesname='Canis lupus',
        speciesname='Canis lupus',
        group='Mammals',
    )
    factories.SpeciesManualAssessmentFactory(region='ALP')
    factories.SpeciesManualAssessmentFactory(
        region='ALP',
        user_id='conclusion_user'
    )
    factories.EtcDicBiogeoregFactory()

    factories.EtcDicHdHabitat()
    factories.HabitattypesManualAssessmentsFactory(region='ALP')
    factories.HabitattypesManualAssessmentsFactory(
        region='ALP',
        user_id='conclusion_user'
    )
    models.db.session.commit()


@pytest.fixture
def setup(app):
    factories.CommentFactory(region='ALP')
    factories.CommentFactory(id=2, author_id='user2', region='ALP')
    factories.CommentFactory(
        id=3,
        author_id='user3',
        region='ALP',
        user_id='conclusion_user'
    )
    factories.WikiFactory(region_code='ALP')
    factories.WikiChangeFactory()
    factories.WikiCommentFactory()

    factories.HabitatCommentFactory(region='ALP')
    factories.HabitatCommentFactory(id=2, author_id='user2', region='ALP')
    factories.HabitatCommentFactory(
        id=3,
        author_id='user3',
        region='ALP',
        user_id='conclusion_user'
    )
    factories.WikiFactory(
        id=2,
        region_code='ALP',
        habitatcode=1110,
        assesment_speciesname=None,
    )
    factories.WikiChangeFactory(
        id=2,
        wiki_id=2,
        body='The conservation status in the marine Baltic region',
    )
    factories.WikiCommentFactory(id=2, wiki_id=2)
    models.db.session.commit()


@pytest.fixture
def setup_deleted(app):
    factories.CommentFactory(id=4, author_id='user4', region='ALP', deleted=1)
    factories.CommentFactory(id=5, author_id='user4', region='ALP', deleted=1,
                   user_id='conclusion_user')
    factories.WikiCommentFactory(id=3, author_id='user3', deleted=1)
    factories.HabitatCommentFactory(id=4, author_id='user4', region='ALP', deleted=1)
    factories.HabitatCommentFactory(id=5, author_id='user4', region='ALP', deleted=1,
                          user_id='conclusion_user')
    factories.WikiCommentFactory(id=4, wiki_id=2, author_id='user4', deleted=1)


@pytest.mark.xfail
@pytest.mark.parametrize(
    "user, path, args",
    [('someuser', '/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'}),
     ('someuser', '/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'}),
     ])
def test_unread_conclusion_comments(app, client, plone_auth, setup_common,
                                    setup, user, path, args):
    create_user(user)
    plone_auth.update({'user_id': user})
    resp = client.get(path, args)
    assert resp.status_code == 200
    assert 'Unread comments for my conclusions: 2' in resp.text
    assert 'Unread comments for all conclusions: 3' in resp.text
    assert 'Unread comments for data sheet info: 1' in resp.text


@pytest.mark.xfail
@pytest.mark.parametrize(
    "path, args",
    [('/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'}),
     ('/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'}),
     ])
def test_unread_conclusion_comments_anonymous_user(
        app, client, plone_auth, setup, path, args):
    resp = client.get(path, args)
    assert resp.status_code == 200
    assert 'Unread comments for my conclusions:' not in resp.text
    assert 'Unread comments for all conclusions:' not in resp.text
    assert 'Unread comments for data sheet info:' not in resp.text


@pytest.mark.xfail
@pytest.mark.parametrize(
    "user, path, args",
    [('someuser', '/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'}),
     ('someuser', '/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'}),
     ])
def test_unread_conclusion_comments_zero_comments(
        app, client, plone_auth, setup_common, user, path, args):
    create_user(user)
    plone_auth.update({'user_id': user})
    resp = client.get(path, args)
    assert resp.status_code == 200
    assert 'Unread comments for my conclusions: 0' in resp.text
    assert 'Unread comments for all conclusions: 0' in resp.text
    assert 'Unread comments for data sheet info: 0' in resp.text


@pytest.mark.xfail
@pytest.mark.parametrize(
    "user, path, args",
    [('someuser', '/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'}),
     ('someuser', '/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'}),
     ])
def test_unread_conclusion_comments_deleted_comments(
        app, client, plone_auth, setup_common, setup, setup_deleted, user,
        path, args):
    create_user(user)
    plone_auth.update({'user_id': user})
    resp = client.get(path, args)
    assert resp.status_code == 200
    assert 'Unread comments for my conclusions: 2' in resp.text
    assert 'Unread comments for all conclusions: 3' in resp.text
    assert 'Unread comments for data sheet info: 1' in resp.text


@pytest.mark.xfail
@pytest.mark.parametrize(
    "username, path, args, comment_cls, wiki_id, read, unread_comments",
    [('someuser', '/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'},
      factories.CommentFactory, 1, True, (2, 3, 1)),
     ('someuser', '/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'},
         factories.HabitatCommentFactory, 2, True, (2, 3, 1)),
     ('someuser', '/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'},
         factories.CommentFactory, 1, False, (3, 5, 2)),
     ('someuser', '/habitat/progress/', {
         'period': '1', 'group': 'coastal habitats', 'conclusion': 'area'},
         factories.HabitatCommentFactory, 2, False, (3, 5, 2)),
     ])
def test_unread_conclusion_comments_read_comments(
        app, client, plone_auth, setup_common, setup, username, path, args,
        comment_cls, wiki_id, read, unread_comments):
    user = create_user(username)
    plone_auth.update({'user_id': username})

    comment = comment_cls(id=10, author_id='user10', region='ALP')
    comment_other_conclusion = comment_cls(
        id=11, author_id='user11', region='ALP', user_id='conclusion_user')
    wiki_comment = factories.WikiCommentFactory(
        id=10, author_id='user10', wiki_id=wiki_id)
    models.db.session.commit()

    if read:
        comment.readers.append(user)
        comment_other_conclusion.readers.append(user)
        wiki_comment.readers.append(user)
        models.db.session.commit()

    resp = client.get(path, args)
    assert resp.status_code == 200
    mine, all, dsi = unread_comments
    assert 'Unread comments for my conclusions: {0}'.format(mine) in resp.text
    assert 'Unread comments for all conclusions: {0}'.format(all) in resp.text
    assert 'Unread comments for data sheet info: {0}'.format(dsi) in resp.text
