'''
clients/__init__.py
This module initializes the clients blueprint for the rental application.
It sets up the blueprint for handling client-related routes and views.
'''

from flask import Blueprint
from rental_app.clients import routes

clients_bp = Blueprint('clients', __name__, template_folder='templates')
