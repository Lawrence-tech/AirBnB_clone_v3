#!/usr/bin/python3
"""module app.prepare flask app"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(app_views)


# Register the teardown handler
@app.teardown_appcontext
def teardown_handler(exception=None):
    """Teardown method to handle storage.close"""
    storage.close()


if __name__ == "__main__":
    # set host and port based on environment variables or defaults
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run Flask app with specified port, host
    app.run(host=host, port=port, threaded=True)
