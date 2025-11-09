# blueprints/configs.py

from flask import Blueprint, jsonify
from logger_config import get_logger

# Blueprint untuk konfigurasi aplikasi
configs_bp = Blueprint('configs', __name__, url_prefix='/api/v1/configs')
logger = get_logger('ConfigsBlueprint')

@configs_bp.route('/splash', methods=['GET'])
def get_splash_config():
    """Endpoint untuk mendapatkan konfigurasi splash screen."""
    try:
        config = {
            "enabled": True,
            "duration": 3000,
            "image_url": "https://example.com/splash.png"
        }
        logger.info("Berhasil mengambil konfigurasi splash.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi splash: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@configs_bp.route('/popup', methods=['GET'])
def get_popup_config():
    """Endpoint untuk mendapatkan konfigurasi popup."""
    try:
        config = {
            "enabled": False,
            "message": "",
            "image_url": ""
        }
        logger.info("Berhasil mengambil konfigurasi popup.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi popup: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@configs_bp.route('/welcome', methods=['GET'])
def get_welcome_config():
    """Endpoint untuk mendapatkan konfigurasi welcome screen."""
    try:
        config = {
            "enabled": True,
            "screens": [
                {
                    "title": "Selamat Datang",
                    "description": "Selamat datang di dieHantar",
                    "image_url": "https://example.com/welcome1.png"
                }
            ]
        }
        logger.info("Berhasil mengambil konfigurasi welcome.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi welcome: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@configs_bp.route('/ads', methods=['GET'])
def get_ads_config():
    """Endpoint untuk mendapatkan konfigurasi iklan."""
    try:
        config = {
            "enabled": False,
            "ads": []
        }
        logger.info("Berhasil mengambil konfigurasi ads.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi ads: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@configs_bp.route('/map', methods=['GET'])
def get_map_config():
    """Endpoint untuk mendapatkan konfigurasi peta."""
    try:
        config = {
            "default_center": {
                "lat": -6.2088,
                "lng": 106.8456
            },
            "default_zoom": 12,
            "map_style": "default"
        }
        logger.info("Berhasil mengambil konfigurasi map.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi map: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@configs_bp.route('/brand', methods=['GET'])
def get_brand_config():
    """Endpoint untuk mendapatkan konfigurasi brand."""
    try:
        config = {
            "app_name": "dieHantar",
            "logo_url": "https://example.com/logo.png",
            "primary_color": "#FF6B6B",
            "secondary_color": "#4ECDC4"
        }
        logger.info("Berhasil mengambil konfigurasi brand.")
        return jsonify({"success": True, "data": config}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil konfigurasi brand: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
