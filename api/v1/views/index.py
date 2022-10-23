#!/usr/bin/python3
"""{add documentation later}"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def get_status():
    """get the current status"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """get the current count"""
    dict1 = {}
    for k, v in classes.items():
        count = storage.count(v)
        dict1.update({k: count})
    return jsonify(dict1)
