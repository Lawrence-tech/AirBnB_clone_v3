#!/usr/bin/python3
"""States app view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def all_states():
    """Returns a list of all states"""
    states_list = []
    states = storage.all("State").values()
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Returns an instance of the specified state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes the specified state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates the specified state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
