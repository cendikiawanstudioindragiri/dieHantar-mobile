# blueprints/broadcasts.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required

# Blueprint untuk broadcasts/announcements
broadcasts_bp = Blueprint('broadcasts', __name__, url_prefix='/api/v1/broadcasts')
logger = get_logger('BroadcastsBlueprint')

@broadcasts_bp.route('/', methods=['GET'])
def get_broadcasts():
    """Endpoint untuk mendapatkan daftar broadcasts/pengumuman."""
    try:
        # Stub implementation - returns empty list for now
        broadcasts_list = []
        logger.info("Berhasil mengambil daftar broadcasts.")
        return jsonify({
            "success": True,
            "data": broadcasts_list,
            "message": "Daftar broadcasts berhasil diambil."
        }), 200
    except Exception as e:
        logger.error(f"Gagal mengambil broadcasts: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@broadcasts_bp.route('/', methods=['POST'])
@token_required
def create_broadcast(uid):
    """Endpoint untuk membuat broadcast baru (placeholder)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        # Stub implementation - placeholder for future functionality
        logger.info(f"UID {uid} mencoba membuat broadcast.")
        return jsonify({
            "success": True,
            "message": "Broadcast berhasil dibuat (placeholder).",
            "data": {
                "id": "broadcast_placeholder_id",
                "title": data.get('title', 'Untitled'),
                "message": data.get('message', ''),
                "created_by": uid
            }
        }), 201
    except Exception as e:
        logger.error(f"Gagal membuat broadcast: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
