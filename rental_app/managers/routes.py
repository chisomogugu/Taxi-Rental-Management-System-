from flask import Blueprint, render_template

managers_bp = Blueprint('managers', __name__)

@managers_bp.route('/dashboard')
def dashboard():
    return render_template('managers/dashboard.html')

@managers_bp.route('/dashboard/top_k_clients')
def top_k_clients():
    return render_template('managers/top_k_clients.html')

@managers_bp.route('/dashboard/model_usage_stats')
def model_usage_stats():
    return render_template('managers/model_usage_stats.html')

@managers_bp.route('/dashboard/driver_performance')
def driver_performance():
    return render_template('managers/driver_performance.html')

@managers_bp.route('/dashboard/cross_city_clients')
def cross_city_clients():
    return render_template('managers/cross_city_clients.html')

@managers_bp.route('/dashboard/add_car')
def add_car():
    return render_template('managers/add_car.html')

@managers_bp.route('/dashboard/remove_car')
def remove_car():
    return render_template('managers/remove_car.html')

@managers_bp.route('/dashboard/add_model')
def add_model():
    return render_template('managers/add_model.html')

@managers_bp.route('/dashboard/remove_model')
def remove_model():
    return render_template('managers/remove_model.html')
