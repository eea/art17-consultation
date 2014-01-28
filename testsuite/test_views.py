
def test_homepage(app, client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_species_summary_view_1(app, client):
    resp = client.get('/species/summary/',
                      {'group': 'Mammals', 'period': '1',
                       'subject': 'Canis lupus', 'region': ''})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'Canis lupus' in resp.text


def test_species_summary_view_2(app, client):
    resp = client.get('/species/summary/',
                      {'group': 'Mammals', 'period': '1',
                       'subject': 'Capra ibex', 'region': ''})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'Canis lupus' not in resp.text


def test_species_progress_view_1(app, client):
    resp = client.get('/species/progress/', {'period': '1', 'group': 'Mammals',
                                             'conclusion': 'population'})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'Mammals, population' in resp.text


def test_species_progress_view_2(app, client):
    resp = client.get('/species/progress/', {'period': '1', 'group': 'Fish',
                                             'conclusion': 'range'})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'Mammals, population' not in resp.text


def test_habitat_summary_view_1(app, client):
    resp = client.get('/habitat/summary/', {
        'period': '1', 'group': 'forests', 'subject': '9010', 'region': ''})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'forests, 9010' in resp.text


def test_habitat_summary_view_2(app, client):
    resp = client.get('/habitat/summary/', {
        'period': '1', 'group': 'grasslands', 'subject': '6110', 'region': ''})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'forests, 9010' not in resp.text
