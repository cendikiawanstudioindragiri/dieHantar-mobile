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
    """Endpoint aman untuk driver memperbarui lokasi mereka dengan data real-time."""
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
            lon=data.get('longitude'),
            accuracy=data.get('accuracy'),  # GPS accuracy in meters
            speed=data.get('speed'),        # Speed in km/h
            heading=data.get('heading')     # Direction in degrees
        )
        logger.info(f"Lokasi driver {driver_id} berhasil diperbarui oleh UID {uid}.")
        return jsonify({"success": True, "message": "Lokasi berhasil diperbarui."}), 200

    except ValueError as e:
        logger.warning(f"Pembaruan lokasi oleh UID {uid} untuk driver {driver_id} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 400 # Bad Request
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} memperbarui lokasi driver {driver_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

@drivers_bp.route('/<string:driver_id>/status', methods=['PUT'])
@token_required
def update_driver_status_endpoint(uid, driver_id):
    """Endpoint untuk driver mengubah status (online/offline/busy)."""
    if uid != driver_id:
        logger.warning(f"Akses ditolak: UID {uid} mencoba mengubah status driver {driver_id}.")
        return jsonify({"success": False, "message": "Akses ditolak."}), 403

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        new_status = data.get('status')
        order_id = data.get('order_id')  # Optional, untuk status busy/en_route
        
        service.update_driver_status(
            driver_id=driver_id,
            new_status=new_status,
            order_id=order_id
        )
        
        logger.info(f"Status driver {driver_id} berhasil diubah ke {new_status} oleh UID {uid}.")
        return jsonify({"success": True, "message": f"Status berhasil diubah ke {new_status}."}), 200

    except ValueError as e:
        logger.warning(f"Update status driver {driver_id} oleh UID {uid} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat update status driver {driver_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

@drivers_bp.route('/nearby', methods=['POST'])
@token_required
def find_nearby_drivers_endpoint(uid):
    """Endpoint untuk mencari driver terdekat dari lokasi tertentu."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        pickup_lat = data.get('pickup_latitude')
        pickup_lon = data.get('pickup_longitude')
        max_distance = data.get('max_distance_km', 10.0)
        vehicle_type = data.get('vehicle_type')
        limit = min(int(data.get('limit', 10)), 50)  # Max 50 drivers

        if not pickup_lat or not pickup_lon:
            return jsonify({
                "success": False, 
                "message": "Koordinat pickup (pickup_latitude, pickup_longitude) diperlukan."
            }), 400

        nearby_drivers = service.find_nearby_drivers(
            pickup_lat=pickup_lat,
            pickup_lon=pickup_lon,
            max_distance_km=max_distance,
            vehicle_type=vehicle_type,
            limit=limit
        )

        drivers_data = [driver.to_dict() for driver in nearby_drivers]

        logger.info(f"UID {uid} mencari driver terdekat: ditemukan {len(drivers_data)} driver.")
        return jsonify({
            "success": True,
            "data": {
                "drivers": drivers_data,
                "total_found": len(drivers_data),
                "search_params": {
                    "pickup_location": {"lat": pickup_lat, "lon": pickup_lon},
                    "max_distance_km": max_distance,
                    "vehicle_type": vehicle_type
                }
            }
        }), 200

    except Exception as e:
        logger.error(f"Error finding nearby drivers for UID {uid}: {e}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": "Terjadi kesalahan saat mencari driver terdekat."
        }), 500

@drivers_bp.route('/<string:driver_id>/eta', methods=['POST'])
@token_required
def calculate_driver_eta_endpoint(uid, driver_id):
    """Endpoint untuk menghitung ETA driver ke lokasi tujuan."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        dest_lat = data.get('destination_latitude')
        dest_lon = data.get('destination_longitude')

        if not dest_lat or not dest_lon:
            return jsonify({
                "success": False,
                "message": "Koordinat tujuan (destination_latitude, destination_longitude) diperlukan."
            }), 400

        eta_info = service.calculate_driver_eta(
            driver_id=driver_id,
            destination_lat=dest_lat,
            destination_lon=dest_lon
        )

        if not eta_info:
            return jsonify({
                "success": False,
                "message": "Tidak dapat menghitung ETA. Driver mungkin offline atau lokasi tidak tersedia."
            }), 404

        logger.info(f"ETA calculated for driver {driver_id} by UID {uid}: {eta_info['eta_minutes']} minutes")
        return jsonify({
            "success": True,
            "data": eta_info
        }), 200

    except Exception as e:
        logger.error(f"Error calculating ETA for driver {driver_id}: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Terjadi kesalahan saat menghitung ETA."
        }), 500

@drivers_bp.route('/<string:driver_id>/location/history', methods=['GET'])
@token_required
def get_driver_location_history_endpoint(uid, driver_id):
    """Endpoint untuk mendapatkan riwayat lokasi driver (untuk tracking real-time)."""
    
    # TODO: Add proper permission check (customer dapat akses jika ada order aktif dengan driver ini)
    
    try:
        limit = min(int(request.args.get('limit', 20)), 100)  # Max 100 locations
        
        location_history = service.get_driver_location_history(
            driver_id=driver_id,
            limit=limit
        )

        return jsonify({
            "success": True,
            "data": {
                "driver_id": driver_id,
                "location_history": location_history,
                "total_points": len(location_history)
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting location history for driver {driver_id}: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Terjadi kesalahan saat mengambil riwayat lokasi."
        }), 500
