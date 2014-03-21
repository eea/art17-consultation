import pytest


def test_homepage(app, client):
    resp = client.get('/')
    assert resp.status_code == 200


@pytest.mark.parametrize("path,args_dict,search_text,elem_found", [
    ('/species/summary/', {}, 'Please select ', True),

    ('/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Canis lupus',
        'region': ''}, 'Canis lupus', True),

    ('/species/summary/', {
        'group': 'Mammals', 'period': '1', 'subject': 'Capra ibex',
        'region': ''}, 'Canis lupus', False),

    ('/species/progress/', {}, 'Please select ', True),

    ('/species/progress/', {
        'period': '1', 'group': 'Mammals', 'conclusion': 'population'},
     'Mammals, population', True),

    ('/species/progress/', {
        'period': '1', 'group': 'Fish', 'conclusion': 'range'},
     'Mammals, population', False),

    ('/species/report/', {}, 'Please select ', True),

    ('/species/report/', {
        'period': '1', 'group': 'Mammals', 'country': 'IT', 'region': ''},
     'Mammals, IT', True),

    ('/species/report/', {
        'period': '1', 'group': 'Fish', 'country': 'EL', 'region': ''},
     'Mammals, IT', False),

    ('/habitat/summary/', {}, 'Please select ', True),

    ('/habitat/summary/', {
        'period': '1', 'group': 'forests', 'subject': '9010', 'region': ''},
     'forests, 9010', True),

    ('/habitat/summary/', {
        'period': '1', 'group': 'grasslands', 'subject': '6110', 'region': ''},
     'forests, 9010', False),

    ('/habitat/progress/', {}, 'Please select ', True),

    ('/habitat/progress/', {
        'period': 1, 'group': 'Forests', 'conclusion': 'range'},
     'Forests, range', True),

    ('/habitat/progress/', {
        'period': 1, 'group': 'Grasslands', 'conclusion': 'area'},
     'Forests, range', False),

    ('/habitat/report/', {}, 'Please select ', True),

    ('/habitat/report/', {
        'period': '1', 'group': 'Forests', 'country': 'IT', 'region': ''},
     'Forests, IT', True),

    ('/habitat/report/', {
        'period': '1', 'group': 'Grasslands', 'country': 'EL', 'region': ''},
     'Forests, IT', False),
])
def test_view(app, client, path, args_dict, search_text, elem_found):
    resp = client.get(path, args_dict)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert (search_text in resp.text) == elem_found
