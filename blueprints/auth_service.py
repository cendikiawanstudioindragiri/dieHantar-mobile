# blueprints/auth_service.py

from functools import wraps
from flask import request, jsonify
from firebase_admin import auth, firestore
from logger_config import get_logger
from firebase_config import get_firestore_client, get_auth_client

logger = get_logger('AuthService')
db = get_firestore_client()
auth_client = get_auth_client()

def create_user_profile(uid: str, email: str, display_name: str) -> dict:
    """
    Membuat dokumen profil pengguna di Firestore setelah berhasil mendaftar di Firebase Auth.
    Fungsi ini bersifat idempotent.
    """
    user_ref = db.collection('users').document(uid)
    
    if user_ref.get().exists:
        logger.info(f"Profil pengguna untuk UID {uid} sudah ada. Melewati pembuatan.")
        return user_ref.get().to_dict()

    logger.info(f"Membuat profil pengguna baru di Firestore untuk UID: {uid}")
    user_data = {
        'email': email,
        'display_name': display_name,
        'uid': uid,
        'role': 'customer',  # Peran default untuk semua pengguna baru
        'created_at': firestore.SERVER_TIMESTAMP,
        'fcm_token': None # Akan diisi oleh klien saat login
    }
    
    try:
        user_ref.set(user_data)
        logger.info(f"Profil pengguna untuk UID {uid} berhasil dibuat.")
        return user_data
    except Exception as e:
        logger.error(f"Gagal membuat profil pengguna untuk UID {uid}: {e}", exc_info=True)
        # Jika pembuatan profil gagal, idealnya kita hapus pengguna dari Firebase Auth
        # untuk menjaga konsistensi data. Ini mencegah pengguna "yatim".
        try:
            auth_client.delete_user(uid)
            logger.warning(f"Pengguna Auth dengan UID {uid} telah dihapus karena kegagalan pembuatan profil.")
        except Exception as delete_e:
            logger.error(f"KRITIS: Gagal menghapus pengguna Auth {uid} setelah kegagalan pembuatan profil: {delete_e}")
        raise e # Sebarkan pengecualian asli

def token_required(f):
    """
    Dekorator untuk memverifikasi Firebase ID Token yang dikirim dalam header Authorization.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            logger.warning("Permintaan ditolak: Header otentikasi tidak ada atau salah format.")
            return jsonify({"success": False, "message": "Header otentikasi 'Bearer <token>' tidak ditemukan."}), 401

        try:
            decoded_token = auth_client.verify_id_token(token)
            kwargs['uid'] = decoded_token['uid']
            logger.info(f"Token berhasil diverifikasi untuk UID: {kwargs['uid']}")
        except auth.ExpiredIdTokenError:
            logger.warning("Token otentikasi telah kedaluwarsa.")
            return jsonify({"success": False, "message": "Token telah kedaluwarsa, silakan login kembali."}), 401
        except auth.InvalidIdTokenError as e:
            logger.error(f"Token otentikasi tidak valid: {e}")
            return jsonify({"success": False, "message": "Token otentikasi tidak valid."}), 401
        except Exception as e:
            logger.error(f"Kesalahan verifikasi token yang tidak terduga: {e}", exc_info=True)
            return jsonify({"success": False, "message": "Gagal memverifikasi otentikasi."}), 500

        return f(*args, **kwargs)

    return decorated_function
