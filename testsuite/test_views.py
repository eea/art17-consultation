
def test_homepage(app, client):
    resp = client.get('/')
    assert resp.status_code == 200


def test_species_summary_view(app, client):
    resp = client.get('/species/summary/',
                      {'group': 'Mammals', 'period': '1',
                       'subject': 'Canis lupus', 'region': ''})
    assert resp.status_code == 200
    assert resp.content_type == 'text/html'
    assert 'Canis lupus' in resp.html.find('caption').text
