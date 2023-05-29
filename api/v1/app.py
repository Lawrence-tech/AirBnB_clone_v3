#!/usr/bin/python3
"""module app.prepare flask app"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
# Register the blueprint
app.register_blueprint(app_views)
CORS(app_views)


# Register the teardown handler
@app.teardown_appcontext
def teardown_handler(error):
    """Teardown method to handle storage.close"""
    storage.close()


if __name__ == "__main__":
    # set host and port based on environment variables or defaults
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    # Run Flask app with specified port, host
    app.run(host=host, port=port, threaded=True, debug=True)
