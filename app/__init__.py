"""Flask application factory."""
from flask import Flask
from config import get_config
from app.models import db


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        app.config.from_object(config_by_name.get(config_name, get_config()))
    else:
        app.config.from_object(get_config())
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes.inventory import inventory_bp
    from app.routes.external import external_bp
    
    app.register_blueprint(inventory_bp, url_prefix='/api')
    app.register_blueprint(external_bp, url_prefix='/api/external')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


# Import config for create_app
from config import config_by_name