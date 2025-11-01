# main.py

import os
from flask import Flask, jsonify
from firebase_config import initialize_firebase

# --- Application Factory ---
def create_app():
    """Membuat dan mengonfigurasi instance aplikasi Flask."""
    # Inisialisasi Firebase Admin SDK
    initialize_firebase()

    app = Flask(__name__)

    # Impor blueprint di dalam factory untuk menghindari circular imports
    from blueprints.auth import auth_bp
    from blueprints.rides import rides_bp
    from blueprints.drivers import drivers_bp
    from blueprints.chats import chats_bp
    from blueprints.orders import orders_bp
    from blueprints.payments import payments_bp
    from blueprints.data_catalog import data_catalog_bp

    # Daftarkan semua blueprint dengan prefix API v1 yang konsisten
    # Catatan: Beberapa blueprint sudah memiliki prefix internal, jadi kita hanya mendaftarkannya.
    app.register_blueprint(auth_bp) # prefix /api/v1/auth ada di dalam blueprint
    app.register_blueprint(rides_bp) # prefix /api/v1/rides ada di dalam blueprint
    app.register_blueprint(drivers_bp) # prefix /api/v1/drivers ada di dalam blueprint
    app.register_blueprint(chats_bp) # prefix /api/v1/chats ada di dalam blueprint
    app.register_blueprint(orders_bp) # prefix /api/v1/orders ada di dalam blueprint
    app.register_blueprint(payments_bp) # prefix /api/v1/payments ada di dalam blueprint
    app.register_blueprint(data_catalog_bp) # prefix /api/v1/catalog ada di dalam blueprint

    @app.route("/")
    def health_check():
        """Endpoint health check untuk memverifikasi bahwa layanan berjalan."""
        return jsonify({"status": "ok", "service": "dieHantar Super-App API"}), 200

    return app

# --- Production Entry Point ---
# Server WSGI seperti Gunicorn akan mencari objek 'app' ini.
app = create_app()
