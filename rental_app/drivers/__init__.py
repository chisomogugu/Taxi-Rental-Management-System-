'''
drivers/__init__.py
This module initializes the drivers blueprint for the rental application.
It sets up the blueprint for handling client-related routes and views.
'''

from flask import Blueprint
from rental_app.drivers import routes

drivers_bp = Blueprint('drivers', __name__, template_folder='templates')
