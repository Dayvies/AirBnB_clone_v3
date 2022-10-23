#!/usr/bin/python3
"""{add function later}"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = "0.0.0.0"
port = 5000

if getenv("HBNB_API_HOST") is not None:
    host = getenv("HBNB_API_HOST")

if getenv("HBNB_API_PORT") is not None:
    port = getenv("HBNB_API_PORT")


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def json_name(error):
    """not json or name missing"""
    return make_response(jsonify({"error": str(error.description)}), 400)


@app.teardown_appcontext
def shutdown_session(exception=None):
    """end session of db"""
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
