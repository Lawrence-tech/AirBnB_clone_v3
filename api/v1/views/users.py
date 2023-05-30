#!/usr/bin/python3
"""users module.Handles User RESTFul API actions"""
from flask import jsonify, Blueprint, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.all('User').values()
    users = [user.to_dict() for user in users]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrives a user object based on id"""
    user = storage.get("User", user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get("User", user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User Object"""
    if not request.json:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in request.json:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in request.json:
        return jsonify({'error': 'Missing password'})
    post_data = request.get_json()
    new_user = User(**post_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get("User", user_id)
    if user:
        if not request.json:
            return jsonify({'error': 'Not a JSON'}), 400
        put_data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for k, v in put_data.items():
            if k not in ignore_keys:
                setattr(user, k, v)
        user.save()
        return jsonify({user.to_dict()}), 200
    else:
        abort(404)
