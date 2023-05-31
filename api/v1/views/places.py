#!/usr/bin/python3
"""Places module.Handles Places RESTFul API actions"""
from flask import jsonify, Blueprint, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    val = []
    for place in city.places:
        val.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrives a place object based on id"""
    place = storage.get("PLace", place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/placess/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get("Place", place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place():
    """Creates a Place Object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    post_data = request.get_json()
    if post_data is None or type(post_data) != dict:
        abort(400, "Not a JSON")
    user_id = post_data.get('user_id')
    if user_id is None:
        abort(400, "Missing user_id")
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    name = post_data.get('name')
    if name is None:
        abort(400, "Missing name")
    place = Place(city_id=city_id, user_id=user_id, name=name)
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    put_data = storage.get_json()
    if put_data is None or type(put_data) != dict:
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in put_data.items():
        if key not in ignored_keys:
            setattr(place, key, value)
            storage.save()
    return jsonify(place.to_dict()), 200
    if state:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        put_data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for k, v in put_data.items():
            if k not in ignore_keys:
                setattr(state, k, v)
        state.save()
        return jsonify({state.to_dict()}), 200
