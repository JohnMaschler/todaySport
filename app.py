from flask import Flask, jsonify
from flask_caching import Cache
from getData import get_final_json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/games": {"origins": "http://localhost:5500"}})

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/games')
@cache.cached(timeout=3600) # cache it for an hour (too long?)
def get_games():
    data = get_final_json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
    
"""
# better for prod?
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache.init_app(app)
"""