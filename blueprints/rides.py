# blueprints/rides.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required
from . import rides_service as service

rides_bp = Blueprint('rides', __name__, url_prefix='/api/v1/rides')
logger = get_logger('RidesBlueprint')

@rides_bp.route('/request', methods=['POST'])
@token_required
def request_new_ride(uid):
    """Endpoint untuk pengguna meminta perjalanan baru."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        ride = service.request_ride(
            user_id=uid,
            pickup=data.get('pickup_location'),
            destination=data.get('destination_location'),
            vehicle=data.get('vehicle_type')
        )
        logger.info(f"Permintaan perjalanan baru {ride.id} berhasil dibuat oleh UID {uid}.")
        return jsonify({"success": True, "message": "Mencari driver...", "ride": ride.to_dict()}), 201
    
    except ValueError as e:
        logger.warning(f"Permintaan perjalanan dari UID {uid} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 400 # Bad Request
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} meminta perjalanan: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500 # Internal Server Error

@rides_bp.route('/<string:ride_id>/accept', methods=['POST'])
@token_required
def accept_ride(uid, ride_id):
    """Endpoint untuk driver menerima tawaran perjalanan."""
    # Di sini, 'uid' dari token adalah ID driver
    driver_id = uid

    try:
        ride = service.accept_ride_offer(driver_id=driver_id, ride_id=ride_id)
        logger.info(f"Driver {driver_id} berhasil menerima perjalanan {ride_id}.")
        return jsonify({"success": True, "message": "Perjalanan diterima.", "ride": ride.to_dict()}), 200

    except ValueError as e:
        logger.warning(f"Driver {driver_id} gagal menerima perjalanan {ride_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 404 # Not Found, karena ride_id tidak ada
    except PermissionError as e:
        logger.warning(f"Driver {driver_id} ditolak menerima perjalanan {ride_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 409 # Conflict, karena status tidak sesuai
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat driver {driver_id} menerima {ride_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

# Hapus file layanan lama untuk kebersihan
