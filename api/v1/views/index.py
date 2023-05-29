#!/usr/bin/python3
"""index module returns a JSON: "status": 'Ok'"""
from flask import jsonify, Blueprint
from api.v1.views import app_views


# Define a route /status on app_views blueprint
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON: "status": 'OK'"""
    return jsonify({"status": "OK"})
