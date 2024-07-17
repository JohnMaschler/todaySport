from flask import Flask, jsonify, request
from flask_caching import Cache
from getData import get_final_json, get_future_games_formatted
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import requests

app = Flask(__name__)
CORS(app)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
@cache.cached(timeout=3600) # cache it for an hour (too long?)
def get_games():
    data = get_final_json()
    return jsonify(data)

@app.route('/future', methods=['GET'])
@cache.cached(timeout=10800)
def get_future_games():
    future_data = get_future_games_formatted()
    return jsonify(future_data)

if __name__ == '__main__':
    app.run(debug=False)
    
"""
# better for prod?
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache.init_app(app)
"""