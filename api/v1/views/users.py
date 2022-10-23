#!/usr/bin/python3
"""handles users"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/users', strict_slashes=False, methods=['POST', 'GET'])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user(user_id=None):
    """retreive users"""
    if request.method == 'GET':
        if user_id is None:
            dict1 = storage.all(User)
            list1 = []
            for k, v in dict1.items():
                list1.append(v.to_dict())
            return jsonify(list1)
        else:
            obj = storage.get(User, user_id)
            if obj is None:
                abort(404)
            else:
                return jsonify(obj.to_dict())
    if request.method == 'DELETE':
        if user_id is None:
            abort(404)
        else:
            obj = storage.get(User, user_id)
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
            abort(400, description="Not a JSON")
        if "email" not in data.keys():
            abort(400, description="Missing email")
        if "password" not in data.keys():
            abort(400, description="Missing password")
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    if request.method == 'PUT':
        obj = storage.get(User, user_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                abort(400, description="Not a JSON")
            list2 = ['id', 'email', 'created_at', 'updated_at']
            for k, v in data.items():
                if k not in list2:
                    setattr(obj, k, v)
            obj.save()
            storage.reload()
            return jsonify(obj.to_dict()), 200
