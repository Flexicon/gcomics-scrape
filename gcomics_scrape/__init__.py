from flask import Flask, jsonify
from gcomics_scrape.routes import api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/v1')

@app.route('/')
def index():
    return jsonify({})

