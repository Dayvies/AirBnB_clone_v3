#!/usr/bin/python3
"""handles states"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/amenities', strict_slashes=False, methods=['POST', 'GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity(amenity_id=None):
    """retreive states"""
    if request.method == 'GET':
        if amenity_id is None:
            dict1 = storage.all(Amenity)
            list1 = []
            for k, v in dict1.items():
                list1.append(v.to_dict())
            return jsonify(list1)
        else:
            obj = storage.get(Amenity, amenity_id)
            if obj is None:
                abort(404)
            else:
                return jsonify(obj.to_dict())
    if request.method == 'DELETE':
        if amenity_id is None:
            abort(404)
        else:
            obj = storage.get(Amenity, amenity_id)
            if obj is None:
                abort(404)
            else:
                storage.delete(obj)
                storage.save()
                return {}, 200
    if request.method == 'POST':
        try:
            data = request.get_json()
            if data is None:
                raise Exception("none data")
        except Exception:
            abort(400, description="Not a JSON")
        if "name" not in data.keys():
            abort(400, description="Missing name")
        new_state = Amenity(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201
    if request.method == 'PUT':
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
                if data is None:
                    raise Exception("none data")
            except Exception:
                abort(400, description="Not a JSON")

            for k, v in data.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(obj, k, v)
            obj.save()
            return jsonify(obj.to_dict()), 200
