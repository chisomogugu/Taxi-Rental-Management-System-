# rental_app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    here = os.path.dirname(__file__)
    template_dir = os.path.abspath(os.path.join(here, '..', 'templates'))
    static_dir   = os.path.abspath(os.path.join(here, '..', 'static'))

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir,
    )

    app.config.from_object(Config)

    db.init_app(app)

    from .home.routes     import home_bp
    from .managers.routes import managers_bp
    from .drivers.routes  import drivers_bp
    from .clients.routes  import clients_bp

    app.register_blueprint(home_bp,     url_prefix='/')
    app.register_blueprint(managers_bp, url_prefix='/manager')
    app.register_blueprint(drivers_bp,  url_prefix='/driver')
    app.register_blueprint(clients_bp,  url_prefix='/client')

    return app
