#!/usr/bin/python3
"""Cities app view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City


@app_views.route("/states/<state_id>/cities")
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    if "name" not in data:
        abort(400, description="Missing name")

    city = City()
    city.name = data["name"]
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)

    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
