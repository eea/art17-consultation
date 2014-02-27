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
    HabitattypesManualAssessmentsFactory
)
from art17 import models
from conftest import get_request_params, create_user


@pytest.fixture
def setup_add(app):
    EtcDicBiogeoregFactory()
    EtcDataSpeciesRegionFactory(
        speciescode='1111',
        assesment_speciesname='Canis lupus')
    EtcDicMethodFactory(order=4, method='2GD')
    EtcDicConclusionFactory()
    DatasetFactory()
    EtcDataHabitattypeRegionFactory(habitatcode=1110)
    EtcDicHdHabitat()
    models.db.session.commit()


@pytest.fixture
def setup_edit(app):
    EtcDicBiogeoregFactory()
    EtcDataSpeciesRegionFactory(
        speciescode='1111',
        assesment_speciesname='Canis lupus')
    EtcDicMethodFactory(order=4, method='2GD')
    EtcDicConclusionFactory()
    DatasetFactory()
    EtcDicHdHabitat()

    EtcDataHabitattypeRegionFactory(habitatcode=1110)
    SpeciesManualAssessmentFactory(region='ALP')
    HabitattypesManualAssessmentsFactory(region='ALP')
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
