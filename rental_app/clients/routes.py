from flask import Blueprint, render_template

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/dashboard')
def dashboard():
    return render_template('clients/dashboard.html')

# add more client-specific endpoints here as needed
