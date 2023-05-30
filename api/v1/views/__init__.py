#!/usr/bin/python3
"""__init__ module."""
from flask import Blueprint


# Create a Blueprint instance for the views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# import views and register them with the Blueprint
if (__name__ == 'api.v1.views'):
    from api.v1.views.index import *
    from api.v1.views.states import *
    from api.v1.views.users import *
