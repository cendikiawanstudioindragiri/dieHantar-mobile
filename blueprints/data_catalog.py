# blueprints/data_catalog.py

from flask import Blueprint, jsonify
from logger_config import get_logger
from . import data_catalog_service as service
from .auth_service import token_required

# Definisikan Blueprint untuk katalog data
data_catalog_bp = Blueprint('data_catalog', __name__, url_prefix='/api/v1/catalog')
logger = get_logger('DataCatalogBlueprint')

@data_catalog_bp.route('/foods', methods=['GET'])
# @token_required # Data makanan mungkin bersifat publik, token bisa jadi opsional.
def get_all_foods():
    """Endpoint untuk mendapatkan semua item makanan."""
    try:
        food_items = service.get_all_food_items()
        # Konversi daftar objek FoodItem menjadi daftar dict
        food_list_dict = [item.to_dict() for item in food_items]
        
        logger.info("Berhasil mengambil semua item makanan.")
        return jsonify({"success": True, "data": food_list_dict}), 200
    except RuntimeError as e:
        logger.error(f"Gagal mengambil item makanan: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        logger.error(f"Kesalahan tak terduga saat mengambil item makanan: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@data_catalog_bp.route('/promotions', methods=['GET'])
# @token_required # Promosi juga mungkin bersifat publik.
def get_all_promotions():
    """Endpoint untuk mendapatkan semua promosi."""
    try:
        promotions = service.get_all_promotions()
        # Konversi daftar objek Promotion menjadi daftar dict
        promo_list_dict = [promo.to_dict() for promo in promotions]

        logger.info("Berhasil mengambil semua promosi.")
        return jsonify({"success": True, "data": promo_list_dict}), 200
    except RuntimeError as e:
        logger.error(f"Gagal mengambil promosi: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
    except Exception as e:
        logger.error(f"Kesalahan tak terduga saat mengambil promosi: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
