# blueprints/drivers.py

from flask import Blueprint, request, jsonify
from . import driver_service as service

# Definisikan Blueprint untuk driver
drivers_bp = Blueprint('drivers_bp', __name__)

# --- Rute untuk Informasi dan Aksi Driver --- #

@drivers_bp.route('/<driver_id>/info', methods=['GET'])
def get_driver_info(driver_id: str):
    """Endpoint untuk mendapatkan informasi publik tentang seorang driver."""
    # TODO: Amankan endpoint ini
    if not driver_id:
        return jsonify({"success": False, "message": "ID Driver dibutuhkan."}), 400

    result = service.get_driver_public_info(driver_id)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 404 # Not Found jika driver tidak ada

# --- Rute untuk Chat --- #

@drivers_bp.route('/chat', methods=['POST'])
def send_message():
    """Endpoint untuk mengirim pesan chat untuk sebuah pesanan."""
    data = request.json
    order_id = data.get('order_id')
    sender_uid = data.get('sender_uid')
    recipient_uid = data.get('recipient_uid')
    message_text = data.get('message_text')

    # TODO: Amankan endpoint ini, verifikasi bahwa sender_uid adalah bagian dari pesanan
    if not all([order_id, sender_uid, recipient_uid, message_text]):
        return jsonify({"success": False, "message": "Data tidak lengkap untuk mengirim pesan."}), 400

    result = service.send_chat_message(order_id, sender_uid, recipient_uid, message_text)
    if result["success"]:
        return jsonify(result), 201
    return jsonify(result), 500

# --- Rute untuk Pencocokan Driver (untuk simulasi) --- #
# Dalam skenario dunia nyata, ini kemungkinan akan menjadi panggilan internal yang dilindungi
# dari layanan pesanan, bukan endpoint publik.

@drivers_bp.route('/match', methods=['POST'])
def match_driver_to_order():
    """
    (Untuk Simulasi) Endpoint untuk memicu pencocokan driver untuk pesanan.
    """
    data = request.json
    order_id = data.get('order_id')
    pickup_location = data.get('pickup_location') # e.g., {'lat': -6.2, 'lon': 106.8}

    if not order_id or not pickup_location:
        return jsonify({"success": False, "message": "ID Pesanan dan lokasi penjemputan dibutuhkan."}), 400

    result = service.find_nearest_driver(order_id, pickup_location)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500
