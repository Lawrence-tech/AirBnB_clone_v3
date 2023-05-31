#!/usr/bin/python3
"""states module.Handles States RESTFul API actions"""
from flask import jsonify, Blueprint, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all('State').values()
    states = [state.to_dict() for state in states]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retives a state object based on id"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State Object"""
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.json:
        return jsonify({'error': 'Missing name'}), 400
    post_data = request.get_json()
    new_state = State(**post_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get("State", state_id)
    if state:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        put_data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for k, v in put_data.items():
            if k not in ignore_keys:
                setattr(state, k, v)
                storage.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
