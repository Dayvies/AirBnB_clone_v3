#!/usr/bin/python3
"""retrieves amenities based on places"""
from models import storage
from models.place import Place
from models.amenity import Amenity
import os
from api.v1.views import app_views
from flask import request, jsonify, abort

db = "fs"
if os.getenv("HBNB_TYPE_STORAGE") == 'db':
    db = "db"


@app_views.route('/places/<place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST', 'DELETE'])
def places_amenities(place_id, amenity_id=None):
    """retrieves amenities based on places"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            amenities = place.amenities
            list1 = []
            for amenity in amenities:
                list1.append(amenity.to_dict())
            return jsonify(list1)
    if request.method == 'DELETE':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if db == 'db':
            if amenity not in place.amenities:
                abort(404)
            else:
                place.amenities.remove(amenity)
                place.save()
                return jsonify({}), 200
        else:
            if amenity.id not in place.amenities:
                abort(404)
            else:
                amenity.place_id = ""
                amenity.save()
                return jsonify({}), 200
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if db == "db":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                place.save()
                storage.save()
                return jsonify(amenity.to_dict()), 201
        else:
            if amenity.id in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                amenity.place_id = place.id
                amenity.save()
                return jsonify(amenity.to_dict()), 201
