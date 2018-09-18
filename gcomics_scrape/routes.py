"""Application routing"""

import requests
import requests_cache
from requests_cache import core as requests_cache_core
from flask import request as req, jsonify, Blueprint, abort

from gcomics_scrape.utils import prepare_comics_list, prepare_comic_dict

# Setup cache
requests_cache.install_cache('comics_cache', expire_after=900)
requests_cache_core.remove_expired_responses()

# Blueprint and base url of the comics api
API_V1 = Blueprint('api_v1', __name__)
BASE_URL = 'https://getcomics.info/wp-json/wp/v2/posts'


@API_V1.route('/comics')
def latest_comics():
    """Retrieve latest comics and serve them in a paginated list"""

    payload = {
        'per_page': req.args.get('limit', None),
        'page': req.args.get('page', None),
        'orderby': 'date',
        '_embed': True
    }
    res = requests.get(BASE_URL, params=payload)
    res.raise_for_status()
    data = res.json()

    return jsonify({
        'data': prepare_comics_list(data),
        'from_cache': res.from_cache,
        'total': res.headers['X-WP-Total'],
        'totalPages': res.headers['X-WP-TotalPages']
    })


@API_V1.route('/comics/search')
def search_comics():
    """Retrieve comics by a given search query and serve them in a paginated list"""

    query = req.args.get('q', None)
    if not query:
        abort(400)

    payload = {
        'search': query,
        'per_page': req.args.get('limit', None),
        'page': req.args.get('page', None),
        'orderby': 'relevance',
        '_embed': True
    }
    res = requests.get(BASE_URL, params=payload)
    res.raise_for_status()
    data = res.json()

    return jsonify({
        'data': prepare_comics_list(data),
        'from_cache': res.from_cache,
        'total': res.headers['X-WP-Total'],
        'totalPages': res.headers['X-WP-TotalPages']
    })


@API_V1.route('/comics/<comic_id>')
def get_comic(comic_id):
    """Retrieve a single comic by a given ID"""

    payload = {'_embed': True}
    res = requests.get(BASE_URL + '/' + comic_id, params=payload)
    res.raise_for_status()
    data = res.json()

    return jsonify({
        'data': prepare_comic_dict(data),
        'from_cache': res.from_cache
    })
