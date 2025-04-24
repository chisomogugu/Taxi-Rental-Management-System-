"""
home/__init__.py
This module initializes the homepage blueprint for the rental application.
"""

from flask import Blueprint
from rental_app.home import routes

home_bp = Blueprint('home', __name__, template_folder='templates')