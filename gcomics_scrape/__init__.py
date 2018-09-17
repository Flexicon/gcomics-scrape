from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from gcomics_scrape.routes import api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')


@app.route('/api')
def index():
    return jsonify({'msg': 'comics api', 'versions': ['v1'], 'resources': ['comics']})


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code
