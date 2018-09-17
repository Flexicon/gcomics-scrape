import pytest

import gcomics_scrape


@pytest.fixture
def client():
    gcomics_scrape.app.config['TESTING'] = True
    client = gcomics_scrape.app.test_client()

    yield client


def test_hello(client):
    """Check if api hello message appears"""

    r = client.get('/api')
    assert r.get_json().get('msg') != None
