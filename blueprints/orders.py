# blueprints/orders.py

from flask import Blueprint, request, jsonify
from . import order_service as service

# Definisikan Blueprint untuk pesanan
orders_bp = Blueprint('orders_bp', __name__, url_prefix='/api/v1/orders')

# --- Rute untuk Kalkulasi dan Pembuatan Pesanan --- #

@orders_bp.route('/calculate', methods=['POST'])
def calculate_order():
    """Endpoint untuk menghitung ringkasan pesanan (subtotal, diskon, total)."""
    data = request.json
    items = data.get('items')
    promotion_code = data.get('promotion_code')

    if not items:
        return jsonify({"success": False, "message": "'items' tidak boleh kosong."}), 400

    summary = service.calculate_order_summary(items, promotion_code)
    return jsonify({"success": True, "summary": summary})

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Endpoint untuk membuat pesanan baru."""
    data = request.json
    uid = data.get('uid')
    order_details = data.get('order_details')

    # TODO: Ganti pengambilan UID dari body dengan verifikasi token otentikasi
    if not uid or not order_details:
        return jsonify({"success": False, "message": "UID dan detail pesanan dibutuhkan."}), 400

    result = service.create_new_order(uid, order_details)
    if result["success"]:
        return jsonify(result), 201  # 201 Created
    return jsonify(result), 500

# --- Rute untuk Riwayat dan Pembatalan Pesanan --- #

@orders_bp.route('/history/<string:uid>', methods=['GET'])
def get_order_history(uid):
    """Endpoint untuk mendapatkan riwayat pesanan pengguna (active, completed, canceled)."""
    # TODO: Amankan endpoint ini dengan verifikasi token.
    order_type = request.args.get('type', 'active') # default ke 'active'
    
    result = service.get_user_orders(uid, order_type)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

@orders_bp.route('/<string:order_id>/cancel', methods=['POST'])
def cancel_single_order(order_id):
    """Endpoint untuk membatalkan pesanan."""
    data = request.json
    uid = data.get('uid')
    reason = data.get('reason', 'Tidak ada alasan diberikan.')

    # TODO: Ganti pengambilan UID dari body dengan verifikasi token.
    if not uid:
        return jsonify({"success": False, "message": "UID dibutuhkan."}), 400

    result = service.cancel_order(order_id, uid, reason)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 400 if "tidak bisa dibatalkan" in result.get("message", "") else 500
