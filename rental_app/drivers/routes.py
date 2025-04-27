from flask import Blueprint, render_template

drivers_bp = Blueprint('drivers', __name__)

@drivers_bp.route('/dashboard')
def dashboard():
    return render_template('drivers/dashboard.html')

# add more driver-specific endpoints here as needed
