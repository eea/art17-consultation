
def test_homepage(app, client):
    resp = client.get('/')
    assert resp.status_code == 200
