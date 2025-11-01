# blueprints/drivers.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required # Kita akan butuh ini untuk mengamankan endpoint
from . import drivers_service as service

drivers_bp = Blueprint('drivers', __name__, url_prefix='/api/v1/drivers')
logger = get_logger('DriversBlueprint')

@drivers_bp.route('/<string:driver_id>/info', methods=['GET'])
def get_driver_info_endpoint(driver_id):
    """Endpoint publik untuk mendapatkan informasi dasar seorang driver."""
    try:
        driver = service.get_driver_public_info(driver_id=driver_id)
        logger.info(f"Berhasil mengambil info untuk driver {driver_id}")
        return jsonify({"success": True, "driver": driver.to_dict()}), 200
    except ValueError as e:
        logger.warning(f"Pengambilan info driver {driver_id} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 404 # Not Found
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat mengambil info driver {driver_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

@drivers_bp.route('/<string:driver_id>/location', methods=['POST'])
@token_required
def update_location_endpoint(uid, driver_id):
    """Endpoint aman untuk driver memperbarui lokasi mereka."""
    # Verifikasi bahwa driver yang diautentikasi (dari token) adalah orang
    # yang sama dengan yang datanya ingin diubah.
    if uid != driver_id:
        logger.warning(f"Akses ditolak: UID {uid} mencoba memperbarui lokasi driver {driver_id}.")
        return jsonify({"success": False, "message": "Akses ditolak."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        service.update_driver_location(
            driver_id=driver_id,
            lat=data.get('latitude'),
            lon=data.get('longitude')
        )
        logger.info(f"Lokasi driver {driver_id} berhasil diperbarui oleh UID {uid}.")
        return jsonify({"success": True, "message": "Lokasi berhasil diperbarui."}), 200

    except ValueError as e:
        logger.warning(f"Pembaruan lokasi oleh UID {uid} untuk driver {driver_id} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 400 # Bad Request
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} memperbarui lokasi driver {driver_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
