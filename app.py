"""Main application file for the dieHantar API."""

import os
from flask import Flask
from dotenv import load_dotenv

# Blueprint imports
from blueprints.data_catalog import data_catalog_bp
from blueprints.order import order_bp
from blueprints.drivers import drivers_bp

# Load environment variables from .env
load_dotenv()


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Application configuration
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-key-default")
    # Add other configurations here if needed

    # Register blueprints
    app.register_blueprint(data_catalog_bp, url_prefix='/api/v1/catalog')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')
    app.register_blueprint(drivers_bp, url_prefix='/api/v1/drivers')

    @app.route("/")
    def index():
        """
        Default route returning a welcome message.
        """
        return "Selamat datang di dieHantar API!"

    return app


if __name__ == "__main__":
    # Create the app instance and run it directly
    app_instance = create_app()
    app_instance.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))