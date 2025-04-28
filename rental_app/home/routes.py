"""
Contains view functions that handle HTTP requests and define URL endpoints for the homepage
"""
from flask import render_template, Blueprint

# homepage blueprint
home_bp = Blueprint('home', __name__, template_folder='templates')


# homepage route
@home_bp.route('/')
def homepage():
    return render_template('home.html')

# about page route
@home_bp.route('/about')
def about():
    return "render_template('about.html')"

# contact page route
@home_bp.route('/contact')
def contact():
    return "render_template('contact.html')"

# terms page route
@home_bp.route('/terms')
def terms():
    return "render_template('terms.html')"