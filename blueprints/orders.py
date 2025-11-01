# blueprints/orders.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required
from . import orders_service as service

orders_bp = Blueprint('orders', __name__, url_prefix='/api/v1/orders')
logger = get_logger('OrdersBlueprint')

@orders_bp.route('/', methods=['POST'])
@token_required
def create_order_endpoint(uid):
    """Endpoint untuk pengguna membuat pesanan makanan baru."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        order = service.create_new_order(
            user_id=uid,
            items_data=data.get('items'),
            address=data.get('delivery_address'),
            promo_code=data.get('promotion_code')
        )
        logger.info(f"Pesanan baru {order.id} berhasil dibuat oleh UID {uid}.")
        return jsonify({"success": True, "message": "Pesanan berhasil dibuat.", "order": order.to_dict()}), 201

    except ValueError as e:
        logger.warning(f"Pembuatan pesanan oleh UID {uid} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 400  # Bad Request
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} membuat pesanan: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500  # Internal Server Error

@orders_bp.route('/<string:order_id>', methods=['GET'])
@token_required
def get_order_endpoint(uid, order_id):
    """Endpoint untuk mendapatkan detail pesanan spesifik."""
    try:
        order = service.get_order_for_user(order_id=order_id, user_id=uid)
        logger.info(f"UID {uid} berhasil mengambil pesanan {order_id}.")
        return jsonify({"success": True, "order": order.to_dict()}), 200

    except ValueError as e:
        logger.warning(f"Pengambilan pesanan {order_id} oleh UID {uid} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 404 # Not Found
    except PermissionError as e:
        logger.warning(f"Akses ditolak untuk UID {uid} pada pesanan {order_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 403 # Forbidden
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} mengambil pesanan {order_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500 # Internal Server Error

