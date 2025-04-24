from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config




db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config) -> Flask:
    """
    Create and configure the Flask application.
    :param config_class: Configuration class to use for the app.
    :return: Configured Flask application instance.
    """
    rental_app = Flask(__name__)
    rental_app.config.from_object(config_class)
    
    db.init_app(rental_app)
    migrate.init_app(rental_app, db)
    
    from rental_app.managers.routes import managers_bp
    from rental_app.clients.routes import clients_bp
    from rental_app.drivers.routes import drivers_bp
    from rental_app.home.routes import home_bp
    
    # Register blueprints
    rental_app.register_blueprint(managers_bp, url_prefix='/manager')
    rental_app.register_blueprint(clients_bp, url_prefix='/client')
    rental_app.register_blueprint(drivers_bp, url_prefix='/driver')
    rental_app.register_blueprint(home_bp, url_prefix='/home')

    
    return rental_app
