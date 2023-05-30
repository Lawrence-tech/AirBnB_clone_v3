#!/usr/bin/python3
"""states module.Handles States RESTFul API actions"""
from flask import jsonify, Blueprint
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all('State').values()
    states = [state.to_dict() for state in states]
    return jsonify(states)

