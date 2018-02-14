import pytest

from . import factories
from art17 import models
from conftest import get_request_params, create_user


def setup_common():
    factories.EtcDicBiogeoregFactory()
    factories.EtcDataSpeciesRegionFactory(
        speciescode='1111',
        assesment_speciesname='Canis lupus')
    factories.EtcDicMethodFactory(order=4, method='2GD')
    factories.EtcDicConclusionFactory()
    factories.DatasetFactory()
    factories.EtcDataHabitattypeRegionFactory(habitatcode=1110)
    factories.EtcDicHdHabitat()


@pytest.fixture
def setup_add(app):
    setup_common()
    factories.EtcDataSpeciesRegionFactory(
        speciescode='1111',
        assesment_speciesname='Canis lupus',
        eu_country_code='FR',
        country='FR',
    )
    factories.EtcDataHabitattypeRegionFactory(
        habitatcode=1110,
        eu_country_code='FR',
        country='FR',
    )
    models.db.session.commit()


@pytest.fixture
def setup_edit(app):
    setup_common()
    factories.SpeciesManualAssessmentFactory(region='ALP')
    factories.HabitattypesManualAssessmentsFactory(region='ALP')
    models.db.session.commit()


@pytest.fixture
def setup_decision(app):
    setup_common()
    factories.SpeciesManualAssessmentFactory(region='ALP')
    factories.HabitattypesManualAssessmentsFactory(region='ALP')
    factories.SpeciesManualAssessmentFactory(decision='OK')
    factories.HabitattypesManualAssessmentsFactory(decision='OK')
    factories.EtcDicDecisionFactory()
    factories.EtcDicDecisionFactory(decision='OK')
    factories.EtcDicDecisionFactory(decision='OK?')
    models.db.session.commit()


@pytest.fixture
def setup_autofill(app):
    setup_common()
    factories.EtcDataSpeciesAutomaticAssessmentFactory(
        assesment_speciesname='Canis lupus',
        region='ALP',
        assessment_method='2GD',
        range_surface_area=100,
        conclusion_range='FV'
    )
    factories.EtcDataHabitattypeAutomaticAssessmentFactory(
        habitatcode='1110',
        region='ALP',
        assessment_method='2GD',
        range_surface_area=100,
        conclusion_range='FV'
    )
    factories.SpeciesManualAssessmentFactory(
        region='ALP',
        range_surface_area=100,
        method_range='2GD',
        conclusion_range='FV'
    )
    factories.HabitattypesManualAssessmentsFactory(
        region='ALP',
        range_surface_area=100,
        method_range='2GD',
        conclusion_range='FV'
    )
    models.db.session.commit()


@pytest.mark.parametrize(
    "request_args, post_params, user, roles, expect_errors, status_code, "
    "search_text",
    # Species
    # STK editing his own conclusion
    [(['/species/summary/', {
        'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
        'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
        'edit_region': 'ALP'}],
     {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'update'}, 'someuser',
        ['stakeholder'], False, 302, 'Conclusion edited successfully'),
     # Editing inexistent conclusion
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'otheruser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 404, ''),
     # STK editing another user's conclusion
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 403, ''),
     # ETC editing his own conclusion
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'someuser', ['etc'], False, 302, 'Conclusion edited successfully'),
     # ETC editing another user's conclusion - Ref fields
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'complementary_favourable_range': '100'},
      'otheruser', ['etc'], False, 302, 'Conclusion edited successfully'),
     # ETC editing another user's conclusion - non-ref fields
     (['/species/summary/', {
         'period': 1, 'group': 'Mammals', 'subject': 'Canis lupus',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'method_population': '2GD', 'conclusion_population': 'FV',
       'submit': 'update'}, 'otheruser', ['etc'], False, 200,
         'Please fill at least one field'),

     # Habitat
     # STK editing his own conclusion
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'}, 'someuser',
         ['stakeholder'], False, 302, 'Conclusion edited successfully'),
     # Editing inexistent conclusion
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'otheruser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 404, ''),
     # STK editing another user's conclusion
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
       'conclusion_population': 'FV', 'submit': 'update'},
      'otheruser', ['stakeholder'], True, 403, ''),
     # ETC editing his own conclusion
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'method_population': '2GD', 'conclusion_population': 'FV',
       'submit': 'update'}, 'someuser', ['etc'], False, 302,
         'Conclusion edited successfully'),
     # ETC editing another user's conclusion - Ref fields
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'complementary_favourable_range': '100', 'submit': 'update'},
      'otheruser', ['etc'], False, 302, 'Conclusion edited successfully'),
     # ETC editing another user's conclusion - non-ref fields
     (['/habitat/summary/', {
         'period': 1, 'group': 'coastal habitats', 'subject': '1110',
         'region': 'ALP', 'action': 'edit', 'edit_user': 'someuser',
         'edit_region': 'ALP'}],
      {'method_population': '2GD', 'conclusion_population': 'FV',
       'submit': 'update'}, 'otheruser', ['etc'], False, 200,
         'Please fill at least one field'),
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
    # assert form['method_range'].value == '2GD'
    # assert form['conclusion_range'].value == 'FV'

    form['complementary_favourable_range'] = '200~~'

    resp = form.submit()
    form = resp.forms[1]

    assert form['range_surface_area'].value == '100'
    # assert form['method_range'].value == '2GD'
    # assert form['conclusion_range'].value == 'FV'

    assert form['complementary_favourable_range'].value == '200~~'
    assert 'form-error-td' in resp.html.find(
        id='complementary_favourable_range').parent.get('class')
    assert resp.html.find('li', {'class': 'flashmessage'}).text == \
        'Please correct the errors below and try again.'


@pytest.mark.parametrize(
    "request_args, post_params, user, MS, roles, model_cls",
    # Species
    [(['/species/summary/', {'period': 1, 'group': 'Mammals',
                             'subject': 'Canis lupus', 'region': 'ALP'}],
     {'region': 'ALP', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'add', 'MS': 'FR'},
      'natuser', 'FR', ['nat'], models.SpeciesManualAssessment),

     # Habitat
     (['/habitat/summary/', {'period': 1, 'group': 'coastal habitats',
                             'subject': '1110', 'region': 'ALP'}],
      {'region': 'ALP', 'method_range': '2GD', 'conclusion_range': 'FV',
       'submit': 'add', 'MS': 'FR'}, 'natuser', 'FR', ['nat'],
      models.HabitattypesManualAssessment),
     ])
def test_add_conclusion_nat(app, client, zope_auth, setup_add, request_args,
                            post_params, user, MS, roles, model_cls):
    create_user(user, roles, ms=MS)
    zope_auth.update({'user_id': user})

    resp = client.post(*get_request_params('post', request_args, post_params))

    assert resp.status_code == 200

    post_params.pop('submit', None)
    manual_ass = model_cls.query.filter_by(**post_params).one()
    assert manual_ass.MS == MS


@pytest.mark.parametrize(
    "request_args, post_params, user, MS, roles, model_cls",
    # Species
    [(['/species/summary/', {'period': 1, 'group': 'Mammals',
                             'subject': 'Canis lupus', 'region': 'ALP'}],
     {'region': 'ALP', 'MS': 'AT', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'add'}, 'stkuser', 'FR',
     ['stakeholder'], models.SpeciesManualAssessment),

     # Habitat
     (['/habitat/summary/', {'period': 1, 'group': 'coastal habitats',
                             'subject': '1110', 'region': 'ALP'}],
      {'region': 'ALP', 'MS': 'AT', 'method_range': '2GD',
       'conclusion_range': 'FV', 'submit': 'add'}, 'stkuser', 'FR',
      ['stakeholder'], models.HabitattypesManualAssessment),
     ])
def test_add_conclusion_stk(app, client, zope_auth, setup_add, request_args,
                            post_params, user, MS, roles, model_cls):
    create_user(user, roles, ms=MS)
    zope_auth.update({'user_id': user})

    resp = client.post(*get_request_params('post', request_args, post_params))

    assert resp.status_code == 200

    post_params.pop('submit', None)
    manual_ass = model_cls.query.filter_by(**post_params).one()
    assert manual_ass.MS == post_params['MS']


@pytest.mark.parametrize(
    "request_args, post_params, user, MS, roles, model_cls",
    # Species
    [(['/species/summary/', {'period': 1, 'group': 'Mammals',
                             'subject': 'Canis lupus', 'region': 'ALP'}],
     {'region': 'ALP', 'method_population': '2GD',
      'conclusion_population': 'FV', 'submit': 'add', 'MS': 'EU27'},
      'etcuser', 'FR', ['etc'], models.SpeciesManualAssessment),

     # Habitat
     (['/habitat/summary/', {'period': 1, 'group': 'coastal habitats',
                             'subject': '1110', 'region': 'ALP'}],
      {'region': 'ALP', 'method_range': '2GD', 'conclusion_range': 'FV',
       'submit': 'add', 'MS': 'EU27'}, 'etcuser', 'FR', ['etc'],
      models.HabitattypesManualAssessment),
     ])
def test_add_conclusion_etc(app, client, zope_auth, setup_add, request_args,
                            post_params, user, MS, roles, model_cls):
    create_user(user, roles, ms=MS)
    zope_auth.update({'user_id': user})

    resp = client.post(*get_request_params('post', request_args, post_params))

    assert resp.status_code == 200

    post_params.pop('submit', None)
    manual_ass = model_cls.query.filter_by(**post_params).one()
    assert manual_ass.MS == 'EU27'


@pytest.mark.parametrize(
    "request_args, user, status_code, expect_errors, model_cls",
    # Species
    # Inexistent record
    [(['/species/conc/delete/', {
        'period': 1, 'subject': 'Canis lupus', 'region': 'ALP',
        'delete_region': 'ALP', 'delete_user': 'someuser', 'delete_ms': 'FR'}],
      'someuser', 404, True, None),
     # Anonymous user
     (['/species/conc/delete/', {
       'period': 1, 'subject': 'Canis lupus', 'region': 'ALP',
       'delete_region': 'ALP', 'delete_user': 'someuser',
       'delete_ms': 'EU27'}], '', 403, True, None),
     # Trying to delete another user's conclusion
     (['/species/conc/delete/', {
       'period': 1, 'subject': 'Canis lupus', 'region': 'ALP',
       'delete_region': 'ALP', 'delete_user': 'someuser',
       'delete_ms': 'EU27'}], 'otheruser', 403, True, None),
     # Successfully deleting its own conclusion
     (['/species/conc/delete/', {
       'period': 1, 'subject': 'Canis lupus', 'region': 'ALP',
       'delete_region': 'ALP', 'delete_user': 'someuser',
       'delete_ms': 'EU27'}], 'someuser', 302, False,
      models.SpeciesManualAssessment),

     # Habitat
     # Inexistent record
     (['/habitat/conc/delete/', {
       'period': 1, 'subject': '1110', 'region': 'ALP', 'delete_region': 'ALP',
       'delete_user': 'someuser', 'delete_ms': 'FR'}],
      'someuser', 404, True, None),
     # Anonymous user
     (['/habitat/conc/delete/', {
       'period': 1, 'subject': '1110', 'region': 'ALP', 'delete_region': 'ALP',
       'delete_user': 'someuser', 'delete_ms': 'EU27'}],
      '', 403, True, None),
     # Trying to delete another user's conclusion
     (['/habitat/conc/delete/', {
       'period': 1, 'subject': '1110', 'region': 'ALP', 'delete_region': 'ALP',
       'delete_user': 'someuser', 'delete_ms': 'EU27'}],
      'otheruser', 403, True, None),
     # Successfully deleting its own conclusion
     (['/habitat/conc/delete/', {
       'period': 1, 'subject': '1110', 'region': 'ALP', 'delete_region': 'ALP',
       'delete_user': 'someuser', 'delete_ms': 'EU27'}],
      'someuser', 302, False, models.HabitattypesManualAssessment),
     ])
def test_delete_conclusion(app, client, zope_auth, setup_edit, request_args,
                           user, status_code, expect_errors, model_cls):
    if user:
        create_user(user)
        zope_auth.update({'user_id': user})

    resp = client.get(*get_request_params('get', request_args),
                      expect_errors=expect_errors)

    assert resp.status_code == status_code

    if model_cls:
        args = request_args[1]
        records = model_cls.query.filter_by(
            dataset_id=args['period'],
            subject=args['subject'],
            region=args['delete_region'],
            user_id=args['delete_user'],
            MS=args['delete_ms'],
        ).all()

        assert len(records) == 1
        assert records[0].deleted == 1


@pytest.mark.parametrize(
    "request_args, post_params, user, roles, expect_errors, status_code, "
    "success, message",
    # Species
    # ETC successfully updating decision
    [(['/species/conc/update/1/Canis lupus/ALP/someuser/', {'ms': 'EU27'}],
      {'decision': 'CO'}, 'testuser', ['etc'], False, 200, True, ''),
     # ADM successfully updating decision
     (['/species/conc/update/1/Canis lupus/ALP/someuser/', {'ms': 'EU27'}],
      {'decision': 'CO'}, 'testuser', ['admin'], False, 200, True, ''),
     # ETC changing a final decision (OK) into another final decision (OK)
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {'decision': 'OK'}, 'testuser', ['etc'], False, 200, False,
      'Another final decision already exists'),
     # ETC selecting invalid decision
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {'decision': 'WTF'}, 'testuser', ['etc'], False, 200, False,
      "'WTF' is not a valid decision."),
     # ETC selecting 'OK?' decision
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {'decision': 'OK?'}, 'testuser', ['etc'], False, 200, False,
      "You are not allowed to select 'OK?'Please select another value."),
     # ETC updating decision - inexistent assessment
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'RAND'}],
      {'decision': 'CO'}, 'testuser', ['etc'], True, 404, '', ''),
     # No decision sent in request
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['etc'], True, 401, '', ''),
     # NAT trying to update decision
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['nat'], True, 403, '', ''),
     # STK trying to update decision
     (['/species/conc/update/1/Canis lupus/BOR/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['stakeholder'], True, 403, '', ''),
     # Habitat
     # ETC successfully updating decision
     (['/habitat/conc/update/1/1110/ALP/someuser/', {'ms': 'EU27'}],
      {'decision': 'CO'}, 'testuser', ['etc'], False, 200, True, ''),
     # ADM successfully updating decision
     (['/habitat/conc/update/1/1110/ALP/someuser/', {'ms': 'EU27'}],
      {'decision': 'CO'}, 'testuser', ['admin'], False, 200, True, ''),
     # ETC changing a final decision (OK) into another final decision (OK)
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {'decision': 'OK'}, 'testuser', ['etc'], False, 200, False,
      'Another final decision already exists'),
     # ETC selecting invalid decision
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {'decision': 'WTF'}, 'testuser', ['etc'], False, 200, False,
      "'WTF' is not a valid decision."),
     # ETC selecting 'OK?' decision
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {'decision': 'OK?'}, 'testuser', ['etc'], False, 200, False,
      "You are not allowed to select 'OK?'Please select another value."),
     # ETC updating decision - inexistent assessment
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'RAND'}],
      {'decision': 'CO'}, 'testuser', ['etc'], True, 404, '', ''),
     # No decision sent in request
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['etc'], True, 401, '', ''),
     # NAT trying to update decision
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['nat'], True, 403, '', ''),
     # STK trying to update decision
     (['/habitat/conc/update/1/1110/MATL/someuser/', {'ms': 'EU27'}],
      {}, 'testuser', ['stakeholder'], True, 403, '', ''),
     ])
def test_update_decision(app, client, zope_auth, setup_decision, request_args,
                         post_params, user, roles, expect_errors, status_code,
                         success, message):
    create_user(user, roles)
    zope_auth.update({'user_id': user})

    resp = client.post(*get_request_params('post', request_args, post_params),
                       expect_errors=expect_errors)

    assert resp.status_code == status_code
    if status_code == 200:
        assert resp.json['success'] == success
        assert resp.json.get('error', '') == message
