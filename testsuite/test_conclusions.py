import pytest

from .factories import (
    EtcDicBiogeoregFactory,
    EtcDataSpeciesRegionFactory,
    EtcDicMethodFactory,
    EtcDicConclusionFactory,
    DatasetFactory,
    EtcDataHabitattypeRegionFactory,
    EtcDicHdHabitat,
    SpeciesManualAssessmentFactory,
    HabitattypesManualAssessmentsFactory,
    EtcDataSpeciesAutomaticAssessmentFactory,
    EtcDataHabitattypeAutomaticAssessmentFactory
)
from art17 import models
from conftest import get_request_params, create_user


def setup_common():
    EtcDicBiogeoregFactory()
    EtcDataSpeciesRegionFactory(
        speciescode='1111',
        assesment_speciesname='Canis lupus')
    EtcDicMethodFactory(order=4, method='2GD')
    EtcDicConclusionFactory()
    DatasetFactory()
    EtcDataHabitattypeRegionFactory(habitatcode=1110)
    EtcDicHdHabitat()


@pytest.fixture
def setup_add(app):
    setup_common()
    models.db.session.commit()


@pytest.fixture
def setup_edit(app):
    setup_common()
    SpeciesManualAssessmentFactory(region='ALP')
    HabitattypesManualAssessmentsFactory(region='ALP')
    models.db.session.commit()


@pytest.fixture
def setup_autofill(app):
    setup_common()
    EtcDataSpeciesAutomaticAssessmentFactory(
        assesment_speciesname='Canis lupus',
        region='ALP',
        assessment_method='2GD',
        range_surface_area=100,
        conclusion_range='FV'
    )
    EtcDataHabitattypeAutomaticAssessmentFactory(
        habitatcode='1110',
        region='ALP',
        assessment_method='2GD',
        range_surface_area=100,
        conclusion_range='FV'
    )
    SpeciesManualAssessmentFactory(
        region='ALP',
        range_surface_area=100,
        method_range='2GD',
        conclusion_range='FV'
    )
    HabitattypesManualAssessmentsFactory(
        region='ALP',
        range_surface_area=100,
        method_range='2GD',
        conclusion_range='FV'
    )
    models.db.session.commit()


@pytest.mark.parametrize(
    "request_args, post_params, roles, expect_errors, status_code, model_cls",
    # Species
    [(['/species/summary/', {'period': 1, 'group': 'Mammals',
                             'subject': 'Canis lupus', 'region': 'ALP'}],
     {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'add'},
     ['stakeholder'], False, 200, models.SpeciesManualAssessment),

     (['/species/summary/', {'period': 1, 'group': 'Mammals',
                             'subject': 'Canis lupus', 'region': 'ALP'}],
      {'region': 'ALP', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'add'},
      ['etc'], True, 403, None),

     # Habitat
     (['/habitat/summary/', {'period': 1, 'group': 'coastal habitats',
                             'subject': '1110', 'region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_range': '2GD',
       'conclusion_range': 'FV', 'submit': 'add'},
      ['stakeholder'], False, 200, models.HabitattypesManualAssessment),

     (['/habitat/summary/', {'period': 1, 'group': 'coastal habitats',
                             'subject': '1110', 'region': 'ALP'}],
      {'region': 'ALP', 'method_range': '2GD',
       'conclusion_range': 'FV', 'submit': 'add'},
      ['etc'], True, 403, None)
     ])
def test_add_conclusion(app, client, zope_auth, setup_add, request_args,
                        post_params, roles, expect_errors, status_code,
                        model_cls):
    create_user('concladd', roles)
    zope_auth.update({'user_id': 'concladd'})

    resp = client.post(*get_request_params('post', request_args, post_params),
                       expect_errors=expect_errors)

    assert resp.status_code == status_code

    if not expect_errors:
        post_params.pop('submit', None)
        assert model_cls.query.filter_by(**post_params).one()


@pytest.mark.parametrize(
    "request_args, post_params, user, roles, expect_errors, status_code, "
    "search_text",
    # Species
    [(['/species/summary/', {
        'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
        'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
        'edit_region': 'ALP'}],
     {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'update'},
     'someuser', ['stakeholder'], False, 302, 'Conclusion edited successfully'),
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'otheruser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 404, ''),
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 403, ''),
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'complementary_favourable_range': '100'},
      'someuser', ['etc'], False, 302, 'Conclusion edited successfully'),

     # Habitat
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'someuser', ['stakeholder'], False, 302, 'Conclusion edited successfully'),
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'otheruser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 404, ''),
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 403, ''),
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'complementary_favourable_range': '100'},
      'someuser', ['etc'], False, 302, 'Conclusion edited successfully'),
     ])
def test_edit_conclusion(app, client, zope_auth, setup_edit, request_args,
                         post_params, user, roles, expect_errors, status_code,
                         search_text):
    create_user(user, roles)
    zope_auth.update({'user_id': user})

    resp = client.post(*get_request_params('post', request_args, post_params),
                       expect_errors=expect_errors)

    assert resp.status_code == status_code

    if resp.status_code == 302:
        resp = resp.follow()

    if search_text:
        assert search_text in resp.html.text


@pytest.mark.parametrize(
    "request_args, user",
    # Species
    # Add conclusion
    [(['/species/summary/', {
        'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
        'region': 'ALP'}], 'newuser'),
     # Edit conclusion
     (['/species/summary/', {
       'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
       'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
       'edit_region': 'ALP'}], 'someuser'),
     # Habitat
     (['/habitat/summary/', {
       'period': 1, 'group': 'coastal habitats', 'subject': '1110',
       'region': 'ALP'}], 'newuser'),
     (['/habitat/summary/', {
       'period': 1, 'group': 'coastal habitats', 'subject': '1110',
       'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
       'edit_region': 'ALP'}], 'someuser')
     ])
def test_autofill_conclusion_form(app, client, zope_auth, setup_autofill,
                                  request_args, user):
    create_user(user, ['stakeholder'])
    zope_auth.update({'user_id': user})

    resp = client.get(*get_request_params('get', request_args))
    form = resp.forms[1]

    assert form['range_surface_area'].value == '100'
    #assert form['method_range'].value == '2GD'
    #assert form['conclusion_range'].value == 'FV'

    form['complementary_favourable_range'] = '200~~'

    resp = form.submit()
    form = resp.forms[1]

    assert form['range_surface_area'].value == '100'
    #assert form['method_range'].value == '2GD'
    #assert form['conclusion_range'].value == 'FV'

    assert form['complementary_favourable_range'].value == '200~~'
    assert 'form-error-td' in resp.html.find(
        id='complementary_favourable_range').parent.get('class')
    assert resp.html.find('li', {'class': 'flashmessage'}).text == \
        'Please correct the errors below and try again.'
