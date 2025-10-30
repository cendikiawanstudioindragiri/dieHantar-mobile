from flask import Blueprint, request, jsonify
from .auth_service import (
    register_user,
    login_user,
    update_user_profile,
    check_onboarding_status,
    set_user_security_setting,
    get_user_profile
)
from logger_config import get_logger

# Inisialisasi Blueprint untuk otentikasi
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
logger = get_logger(__name__)

# Middleware untuk otentikasi (contoh sederhana)
# Dalam aplikasi nyata, gunakan verifikasi token Firebase (misalnya, Bearer token)
@auth_bp.before_request
def before_request_func():
    # Contoh rute yang tidak memerlukan otentikasi
    if request.endpoint in ['auth.register', 'auth.login_phone']:
        return
    
    # Dapatkan ID Token dari header
    id_token = request.headers.get('Authorization')
    if not id_token or not id_token.startswith('Bearer '):
        logger.warning("Akses ditolak: Header Authorization tidak ada atau formatnya salah.")
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    # Di sini Anda akan memverifikasi token dengan Firebase Admin SDK
    # Untuk contoh ini, kita akan melewati verifikasi dan hanya log
    logger.info("Token diterima, lanjutkan ke proses verifikasi (simulasi)...")
    # try:
    #     decoded_token = auth.verify_id_token(id_token.split(' ')[1])
    #     g.user = decoded_token # Simpan info user di global context Flask 'g'
    # except auth.InvalidIdTokenError:
    #     return jsonify({"success": False, "message": "Token tidak valid."}), 401
    # except Exception as e:
    #     return jsonify({"success": False, "message": f"Kesalahan verifikasi token: {e}"}), 500


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint untuk mendaftarkan pengguna baru (C. Signup).
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['phone_number', 'password', 'device_id']):
        return jsonify({"success": False, "message": "Data tidak lengkap."}), 400

    result = register_user(data['phone_number'], data['password'], data['device_id'])
    
    if result.get("success"):
        return jsonify(result), 201
    else:
        # Tentukan status code berdasarkan pesan error
        if "sudah terdaftar" in result.get("message", ""):
            return jsonify(result), 409 # Conflict
        else:
            return jsonify(result), 500 # Server error


@auth_bp.route('/login', methods=['POST'])
def login_phone():
    """
    Endpoint untuk login dan mendapatkan custom token (B. Login).
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['uid', 'device_id']):
        return jsonify({"success": False, "message": "UID dan device_id diperlukan."}), 400

    result = login_user(data['uid'], data['device_id'])
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@auth_bp.route('/onboarding_status/<string:uid>', methods=['GET'])
def get_onboarding_status(uid: str):
    """
    Endpoint untuk memeriksa status onboarding pengguna (A).
    """
    result = check_onboarding_status(uid)
    if result["status"] == "ERROR":
        return jsonify(result), 500
    return jsonify(result), 200


@auth_bp.route('/profile/<string:uid>', methods=['PUT'])
def update_profile(uid: str):
    """
    Endpoint untuk memperbarui profil pengguna (E).
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['full_name', 'email', 'birth_date']):
        return jsonify({"success": False, "message": "Nama, email, dan tanggal lahir diperlukan."}), 400
        
    result = update_user_profile(uid, data['full_name'], data['email'], data['birth_date'])
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500


@auth_bp.route('/profile/<string:uid>', methods=['GET'])
def get_profile(uid: str):
    """
    Endpoint untuk mendapatkan profil pengguna (Y).
    """
    result = get_user_profile(uid)
    if result.get("success"):
        return jsonify(result), 200
    elif "tidak ditemukan" in result.get("message", ""):
        return jsonify(result), 404
    else:
        return jsonify(result), 500


@auth_bp.route('/security_setting/<string:uid>', methods=['PUT'])
def set_security_setting(uid: str):
    """
    Endpoint untuk mengatur PIN atau Touch ID (F/G).
    """
    data = request.get_json()
    if not data or not all(k in data for k in ['security_type', 'is_set']):
        return jsonify({"success": False, "message": "Tipe keamanan dan status diperlukan."}), 400
    
    result = set_user_security_setting(uid, data['security_type'], data['is_set'])
    
    if result.get("success"):
        return jsonify(result), 200
    else:
        return jsonify(result), 500
