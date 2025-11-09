# blueprints/partners.py

from flask import Blueprint, jsonify
from logger_config import get_logger

# Blueprint untuk partners/merchant partners
partners_bp = Blueprint('partners', __name__, url_prefix='/api/v1/partners')
logger = get_logger('PartnersBlueprint')

@partners_bp.route('/', methods=['GET'])
def get_partners():
    """Endpoint untuk mendapatkan daftar mitra/partner."""
    try:
        # Stub implementation - returns empty list for now
        partners_list = []
        logger.info("Berhasil mengambil daftar partners.")
        return jsonify({
            "success": True,
            "data": partners_list,
            "message": "Daftar partners berhasil diambil."
        }), 200
    except Exception as e:
        logger.error(f"Gagal mengambil daftar partners: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@partners_bp.route('/<string:partner_id>', methods=['GET'])
def get_partner_by_id(partner_id):
    """Endpoint untuk mendapatkan detail partner berdasarkan ID."""
    try:
        # Stub implementation - returns placeholder data
        partner_data = {
            "id": partner_id,
            "name": "Partner Placeholder",
            "category": "Restaurant",
            "address": "Jl. Example No. 123",
            "rating": 4.5
        }
        logger.info(f"Berhasil mengambil detail partner {partner_id}.")
        return jsonify({"success": True, "data": partner_data}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil detail partner {partner_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
