from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config

# Global SQLAlchemy instance (initialized with app in create_app)
db = SQLAlchemy()


def create_app(testing: bool = False) -> Flask:
    """Application factory pattern.

    Args:
        testing: If True, use testing configuration (in-memory DB).

    Returns:
        Configured Flask app instance.
    """
    app = Flask(__name__)
    if testing:
        app.config.from_object("app.config.TestingConfig")
    else:
        app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register routes/blueprints
    from .routes import bp as api_bp  # noqa: E402

    app.register_blueprint(api_bp, url_prefix="/")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
