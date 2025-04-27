import os
from flask import Flask

def create_app():
    # compute absolute path to your project-root/templates folder
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'templates')
    )

    app = Flask(
        __name__,
        template_folder=template_dir,  # point Flask at ../templates
        static_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'static')
        ),  # if you ever add a top-level static/
    )

    # import and register each blueprint
    from .home.routes    import home_bp
    from .managers.routes import managers_bp
    from .drivers.routes  import drivers_bp
    from .clients.routes  import clients_bp

    app.register_blueprint(home_bp,     url_prefix='/')
    app.register_blueprint(managers_bp, url_prefix='/manager')
    app.register_blueprint(drivers_bp,  url_prefix='/driver')
    app.register_blueprint(clients_bp,  url_prefix='/client')

    return app
