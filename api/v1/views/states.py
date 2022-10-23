#!/usr/bin/python3
"""handles states"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response


@app_views.route('/states', strict_slashes=False, methods=['POST', 'GET'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state(state_id=None):
    """retreive states"""
    if request.method == 'GET':
        if state_id is None:
            dict1 = storage.all(State)
            list1 = []
            for k, v in dict1.items():
                list1.append(v.to_dict())
            return jsonify(list1)
        else:
            obj = storage.get(State, state_id)
            if obj is None:
                abort(404)
            else:
                return jsonify(obj.to_dict())
    if request.method == 'DELETE':
        if state_id is None:
            abort(404)
        else:
            obj = storage.get(State, state_id)
            if obj is None:
                abort(404)
            else:
                storage.delete(obj)
                storage.save()
                return {}, 200
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            return jsonify({"error": "Not a JSON"}), 400
        if "name" not in data.keys():
            return make_response(jsonify({"error": "Missing name"}), 400)
        new_state = State(**data)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)
    if request.method == 'PUT':
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                return make_response(jsonify({"error": "Not a JSON"}), 400)

            for k, v in data.items():
                if k != 'id' and k != 'created_at' and k != 'updated_at':
                    setattr(obj, k, v)
            obj.save()
            return jsonify(obj.to_dict()), 200
