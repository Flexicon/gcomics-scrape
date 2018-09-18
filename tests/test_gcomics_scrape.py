"""Application tests"""

import pytest
import responses
from responses import Response
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

    responses.add(Response(
        method='GET',
        url=BASE_URL,
        match_querystring=False,
        json=COMICS_RESPONSE,
        headers=COMICS_HEADERS
    ))
    res = client.get('/api/v1/comics').get_json()
    data = res.get('data')

    assert data != None
    assert len(data) == len(COMICS_RESPONSE)
    assert data[0].get('id') == COMICS_RESPONSE[0].get('id')


@responses.activate
def test_comics_limit_per_page(client):
    """Check if /comics with a limit param correctly sets the api limit"""

    responses.add(Response(
        method='GET',
        url=BASE_URL,
        match_querystring=False,
        json=COMICS_RESPONSE,
        headers=COMICS_HEADERS
    ))
    res = client.get('/api/v1/comics?limit=1').get_json()
    data = res.get('data')
    params = res.get('params')

    assert data != None
    assert params != None
    assert params.get('per_page') == '1'
