from flask import request as req, jsonify, Blueprint
from gcomics_scrape.utils import prepare_comics_list, prepare_comic_dict
from datetime import datetime
import requests
import requests_cache
from requests_cache import core as requests_cache_core

BASE_URL = 'https://getcomics.info/wp-json/wp/v2/posts'

requests_cache.install_cache('comics_cache', expire_after=900)
requests_cache_core.remove_expired_responses()

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/comics')
def latest_comics():
    payload = {
        'per_page': req.args.get('limit', None),
        'page': req.args.get('page', None),
        'orderby': 'date',
        '_embed': True
    }
    r = requests.get(BASE_URL, params=payload)
    r.raise_for_status()
    data = r.json()

    return jsonify({
        'data': prepare_comics_list(data),
        'total': r.headers['X-WP-Total'],
        'totalPages': r.headers['X-WP-TotalPages']
    })


@api_v1.route('/comics/search')
def search_comics():
    payload = {
        'search': req.args.get('search', None),
        'per_page': req.args.get('limit', None),
        'page': req.args.get('page', None),
        'orderby': 'relevance',
        '_embed': True
    }
    r = requests.get(BASE_URL, params=payload)
    r.raise_for_status()
    data = r.json()

    return jsonify({
        'data': prepare_comics_list(data),
        'total': r.headers['X-WP-Total'],
        'totalPages': r.headers['X-WP-TotalPages']
    })


@api_v1.route('/comics/<comic_id>')
def get_comic(comic_id):
    payload = {'_embed': True}
    r = requests.get(BASE_URL + '/' + comic_id, params=payload)
    r.raise_for_status()
    data = r.json()

    return jsonify(prepare_comic_dict(data))
