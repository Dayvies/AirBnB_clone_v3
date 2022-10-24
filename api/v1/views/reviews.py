#!/usr/bin/python3
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/places/<place_id>/reviews', strict_slashes=False, methods=['POST', 'GET'])
def places_reviews(place_id):
    """get reviews according to places"""
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            reviews = place.reviews
            list2 = []
        for review in reviews:
            list2.append(review.to_dict())
        return jsonify(list2)
    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                abort(400, description="Not a JSON")
            if "user_id" not in data.keys():
                abort(400, description="Missing user_id")
            if storage.get(User, data.get('user_id')) is None:
                abort(400)
            if 'text' not in data.keys():
                abort(400, description="Missing text")
            data.update({'place_id': place_id})
            new_review = Review(**data)
            new_review.save()
            return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT', 'DELETE', 'GET'])
def get_reviews(review_id):
    """reviews using review_id"""
    if request.method == 'GET':
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        else:
            return jsonify(review.to_dict())
    if request.method == 'DELETE':
        obj = storage.get(Review, review_id)
        if obj is None:
            abort(404)
        else:
            storage.delete(obj)
            storage.save()
            return {}, 200
    if request.method == 'PUT':
        obj = storage.get(Review, review_id)
        if obj is None:
            abort(404)
        else:
            try:
                data = request.get_json()
            except Exception:
                abort(400, description="Not a JSON")
            list2 = ['id', 'user_id', 'created_at', 'updated_at']
            for k, v in data.items():
                if k not in list2:
                    setattr(obj, k, v)
            obj.save()
            return jsonify(obj.to_dict()), 200
