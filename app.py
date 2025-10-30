# app.py

import os
from flask import Flask
from dotenv import load_dotenv

# Muat variabel lingkungan dari .env
load_dotenv()

# Impor dan daftarkan blueprint
from blueprints.data_catalog import data_catalog_bp
from blueprints.order import order_bp
from blueprints.driver import driver_bp


def create_app():
    app = Flask(__name__)

    # Konfigurasi aplikasi (jika ada)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "super-secret-key-default")

    # Daftarkan blueprint
    app.register_blueprint(data_catalog_bp, url_prefix='/api/v1/catalog')
    app.register_blueprint(order_bp, url_prefix='/api/v1/orders')
    app.register_blueprint(driver_bp, url_prefix='/api/v1/drivers')

    @app.route("/")
    def index():
        return "Selamat datang di dieHantar API!"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
