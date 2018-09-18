"""Application tests"""

import responses
import pytest
import gcomics_scrape
from gcomics_scrape.routes import BASE_URL
from tests.mock_responses import COMICS_RESPONSE, COMICS_HEADERS


@pytest.fixture
def client():
    """Prepare app client for testing"""

    gcomics_scrape.APP.config['TESTING'] = True
    test_client = gcomics_scrape.APP.test_client()

    yield test_client


def test_hello(client):
    """Check if api hello message appears"""

    res = client.get('/api')
    assert res.get_json().get('msg') != None


@responses.activate
def test_comics_return_all_from_api(client):
    """Check if /comics returns the comics returned from api as data"""

    responses.add(
        responses.GET, BASE_URL,
        json=COMICS_RESPONSE,
        headers=COMICS_HEADERS
    )
    res = client.get('/api/v1/comics')

    print(res.get_json())
    assert res.get_json().get('data') != None
