# blueprints/auth.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required, create_user_profile
from firebase_config import get_firestore_client

# Blueprint untuk otentikasi dan manajemen profil pengguna
auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
logger = get_logger('AuthBlueprint')
db = get_firestore_client()

@auth_bp.route('/profile/sync', methods=['POST'])
@token_required
def sync_user_profile(uid):
    """
    Endpoint untuk membuat/sinkronisasi profil pengguna di Firestore setelah pendaftaran.
    Klien harus memanggil endpoint ini sekali setelah pendaftaran berhasil.
    Endpoint ini bersifat idempotent.
    """
    data = request.get_json()
    if not data or 'email' not in data:
        logger.warning(f"Permintaan sync profile dari UID {uid} gagal: email tidak ada.")
        return jsonify({"success": False, "message": "Email diperlukan dalam body request."}), 400

    email = data.get('email')
    display_name = data.get('display_name') # Nama tampilan bersifat opsional

    try:
        logger.info(f"Memulai sinkronisasi profil untuk UID: {uid}")
        user_profile = create_user_profile(uid=uid, email=email, display_name=display_name)
        logger.info(f"Profil untuk UID {uid} berhasil disinkronkan.")
        return jsonify({"success": True, "message": "Profil pengguna berhasil disinkronkan.", "profile": user_profile}), 201
    except Exception as e:
        logger.error(f"Gagal saat sinkronisasi profil untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server saat membuat profil."}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_my_profile(uid):
    """
    Endpoint untuk mengambil detail profil pengguna yang sedang login.
    """
    try:
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            logger.warning(f"Profil pengguna untuk UID {uid} tidak ditemukan di Firestore.")
            return jsonify({"success": False, "message": "Profil pengguna tidak ditemukan."}), 404

        logger.info(f"Berhasil mengambil profil untuk UID: {uid}")
        return jsonify({"success": True, "profile": user_doc.to_dict()}), 200

    except Exception as e:
        logger.error(f"Gagal mengambil profil untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
