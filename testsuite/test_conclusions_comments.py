import pytest

from .factories import (
    SpeciesManualAssessmentFactory,
    CommentFactory,
    HabitattypesManualAssessmentsFactory,
    HabitatCommentFactory,
)
from art17 import models
from conftest import get_request_params, create_user


@pytest.fixture
def setup(app):
    SpeciesManualAssessmentFactory()
    CommentFactory()
    HabitattypesManualAssessmentsFactory()
    HabitatCommentFactory()
    models.db.session.commit()


@pytest.mark.parametrize(
    "request_type, request_args, post_params, user, expect_errors, "
    "status_code, assert_condition",
    ## Species
    # Anonymous user
    [('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/', {}],
      {'comment': 'I cannot post comments'}, [], True, 403, ""),
     ('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
               {'edit': 1}],
      {'comment': 'I cannot edit this comment'}, [], True, 403, ""),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, [], True, 403, ""),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, [], True, 403, ""),
     # User that posted a comment already
     ('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/', {}],
      {'comment': 'I cannot post comments'}, ['testuser'], True, 403, ""),
     ('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
               {'edit': 1}],
      {'comment': 'I can edit this comment!'}, ['testuser'], False, 302,
      "'I can edit this comment!' in resp.html.text"),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, ['testuser'], True, 403, ""),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['testuser'], False, 200,
      "'Undelete' in resp.html.text"),
     # User that didn't post any comments
     ('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/', {}],
      {'comment': 'I can post comments!'}, ['newuser'], False, 302,
      "'I can post comments!' in resp.html.text"),
     ('post', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
               {'edit': 1}],
      {'comment': "I can't edit testuser's comment"}, ['newuser'], True, 403,
      ""),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, ['newuser'], False, 200,
      "'Mark as unread' in resp.html.text"),
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['newuser'], True, 403, ""),
     # User with admin role
     ('get', ['/species/comments/1/Canis lupus/BOR/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['adminuser', ['admin']], False, 200,
      "'Undelete' in resp.html.text"),
     ## Habitat
     # Anonymous user
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {}],
      {'comment': 'I cannot post comments'}, [], True, 403, ""),
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {'edit': 1}],
      {'comment': 'I cannot edit this comment'}, [], True, 403, ""),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, [], True, 403, ""),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, [], True, 403, ""),
     # User that posted a comment already
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {}],
      {'comment': 'I cannot post comments'}, ['testuser'], True, 403, ""),
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {'edit': 1}],
      {'comment': 'I can edit this comment!'}, ['testuser'], False, 302,
      "'I can edit this comment!' in resp.html.text"),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, ['testuser'], True, 403, ""),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['testuser'], False, 200,
      "'Undelete' in resp.html.text"),
     # User that didn't post any comments
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {}],
      {'comment': 'I can post comments!'}, ['newuser'], False, 302,
      "'I can post comments!' in resp.html.text"),
     ('post', ['/habitat/comments/1/1110/MATL/someuser/EU25/', {'edit': 1}],
      {'comment': "I can't edit testuser's comment"}, ['newuser'], True, 403,
      ""),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'toggle': 1, 'read': False}], {}, ['newuser'], False, 200,
      "'Mark as unread' in resp.html.text"),
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['newuser'], True, 403, ""),
     # User with admin role
     ('get', ['/habitat/comments/1/1110/MATL/someuser/EU25/',
      {'delete': 1, 'deleted': 0}], {}, ['adminuser', ['admin']], False, 200,
      "'Undelete' in resp.html.text"),
     ])
def test_comments(app, client, setup, zope_auth, request_type, request_args,
                  post_params, user, expect_errors, status_code,
                  assert_condition):
    if user:
        create_user(*user)
        zope_auth.update({'user_id': user[0]})

    resp = getattr(client, request_type)(*get_request_params(
        request_type, request_args, post_params), expect_errors=expect_errors)
    assert resp.status_code == status_code

    if resp.status_code == 302:
        resp = resp.follow()

    if assert_condition:
        assert eval(assert_condition)
