# blueprints/payments.py

from flask import Blueprint, request, jsonify
from . import payment_service as service

# Definisikan Blueprint untuk pembayaran
payments_bp = Blueprint('payments_bp', __name__, url_prefix='/api/v1/payments')

# --- Rute untuk Metode Pembayaran --- #

@payments_bp.route('/methods', methods=['POST'])
def add_payment_method():
    """Endpoint untuk menambahkan metode pembayaran baru (dengan token)."""
    data = request.json
    uid = data.get('uid')
    card_data = data.get('card_data') # e.g., {'token': '...', 'last4': '...′, 'brand': '...'}

    # TODO: Amankan endpoint ini dengan verifikasi token otentikasi
    if not uid or not card_data or 'token' not in card_data:
        return jsonify({"success": False, "message": "UID dan token kartu dibutuhkan."}), 400

    result = service.add_new_payment_method(uid, card_data)
    if result["success"]:
        return jsonify(result), 201
    return jsonify(result), 500

# --- Rute untuk Webhook dari Payment Gateway --- #

@payments_bp.route('/webhook', methods=['POST'])
def payment_webhook():
    """Endpoint untuk menerima notifikasi dari Payment Gateway."""
    payload = request.json
    # TODO: Tambahkan verifikasi signature webhook di sini
    result = service.handle_payment_webhook(payload)
    return jsonify(result), 200

# --- Rute untuk Review dan Tip --- #

@payments_bp.route('/review', methods=['POST'])
def submit_review():
    """Endpoint untuk mengirimkan rating dan review untuk sebuah pesanan."""
    data = request.json
    uid = data.get('uid')
    order_id = data.get('order_id')
    rating_data = data.get('rating_data')

    # TODO: Amankan endpoint ini dan verifikasi kepemilikan pesanan
    if not all([uid, order_id, rating_data]):
        return jsonify({"success": False, "message": "Data tidak lengkap."}), 400

    result = service.submit_order_rating_review(uid, order_id, rating_data)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

@payments_bp.route('/givethanks', methods=['POST'])
def give_thanks():
    """Endpoint untuk memberikan tip kepada driver."""
    data = request.json
    driver_id = data.get('driver_id')
    amount = data.get('amount')

    if not driver_id or not isinstance(amount, int) or amount <= 0:
        return jsonify({"success": False, "message": "ID driver dan jumlah tip yang valid dibutuhkan."}), 400

    # TODO: Integrasikan dengan proses pembayaran tip yang sesungguhnya
    result = service.give_thanks_to_driver(driver_id, amount)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

