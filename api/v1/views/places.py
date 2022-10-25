#!/usr/bin/python3
"""handles citys"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST', 'GET'])
def city_places(city_id):
    """get places depending on city"""
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            places = city.places
            list1 = []
            for place in places:
                list1.append(place.to_dict())
            return jsonify(list1)
    if request.method == 'POST':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            try:
                data = request.get_json()
                if data is None:
                    raise Exception("none data")
            except Exception:
                abort(400, description="Not a JSON")
            if "user_id" not in data.keys():
                abort(400, description="Missing user_id")
            if storage.get(User, data.get('user_id')) is None:
                abort(404)
            if "name" not in data.keys():
                abort(400, description="Missing name")
            data.update({'city_id': city_id})
            new_place = Place(**data)
            new_place.save()
            return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT', 'GET', 'DELETE'])
def places(place_id):
    """get places on id"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            return jsonify(place.to_dict())
    if request.method == 'DELETE':
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        else:
            storage.delete(obj)
            storage.save()
            return jsonify({}), 200
    if request.method == 'PUT':
        obj = storage.get(Place, place_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
                if data is None:
                    raise Exception("none data")
            except Exception:
                abort(400, description="Not a JSON")
            list2 = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for k, v in data.items():
                if k not in list2:
                    setattr(obj, k, v)
            obj.save()
            return jsonify(obj.to_dict()), 200
