#!/usr/bin/python3
"""index module returns a JSON: "status": 'Ok'"""
from flask import jsonify, Blueprint
from api.v1.views import app_views
from models import storage

# Define a route /status on app_views blueprint
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON: "status": 'OK'"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def obj_stats():
    objs = {"amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")}
    return jsonify(objs)

