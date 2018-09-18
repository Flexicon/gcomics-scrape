"""GComics API to commmunicate with and parse comics sources"""

import requests_cache
from requests_cache import core as requests_cache_core
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from gcomics_scrape.routes import API_V1

APP = Flask(__name__)
APP.register_blueprint(API_V1, url_prefix='/api/v1')

# Setup cache
requests_cache.install_cache('comics_cache', expire_after=900)
requests_cache_core.remove_expired_responses()


@APP.route('/api')
def index():
    """Display api information"""
    return jsonify({'msg': 'comics api', 'versions': ['v1'], 'resources': ['comics']})


@APP.errorhandler(Exception)
def handle_error(err):
    """Global application error handler"""

    code = 500
    if isinstance(err, HTTPException):
        code = err.code
    return jsonify(error=str(err)), code
