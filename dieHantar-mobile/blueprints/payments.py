# blueprints/payments.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required
from . import payments_service_new as service
from . import midtrans_service as midtrans

payments_bp = Blueprint('payments', __name__, url_prefix='/api/v1')
logger = get_logger('PaymentsBlueprint')

# blueprints/payments.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required
from . import payments_service_new as service
from . import midtrans_service as midtrans

payments_bp = Blueprint('payments', __name__, url_prefix='/api/v1')
logger = get_logger('PaymentsBlueprint')

@payments_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods_endpoint():
    """Endpoint untuk mendapatkan daftar payment methods yang tersedia."""
    try:
        payment_methods = service.get_payment_methods()
        return jsonify({
            "success": True,
            "data": {
                "payment_methods": payment_methods,
                "total": len(payment_methods)
            }
        }), 200
    except Exception as e:
        logger.error(f"Error getting payment methods: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Terjadi kesalahan saat mengambil payment methods."
        }), 500

@payments_bp.route('/orders/<string:order_id>/pay', methods=['POST'])
@token_required
def initiate_payment_endpoint(uid, order_id):
    """
    Endpoint aman untuk memulai proses pembayaran untuk sebuah pesanan.
    Body: {"payment_method": "snap|gopay|bca_va|etc"}
    """
    try:
        data = request.get_json() or {}
        payment_method = data.get('payment_method', 'snap')
        
        transaction = service.initiate_order_payment(
            order_id=order_id, 
            requester_uid=uid,
            payment_method=payment_method
        )
        
        logger.info(f"Payment transaction {transaction.id} created for order {order_id} via {payment_method}.")
        
        # Prepare response berdasarkan payment method
        response_data = {
            "transaction_id": transaction.id,
            "order_id": order_id,
            "amount": transaction.amount,
            "payment_method": transaction.payment_method,
            "status": "pending",
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None
        }
        
        # Add method-specific data
        if payment_method == "snap":
            response_data.update({
                "snap_token": transaction.snap_token,
                "redirect_url": transaction.redirect_url,
                "message": "Silahkan lanjutkan pembayaran menggunakan Snap."
            })
        else:
            response_data.update({
                "payment_url": transaction.redirect_url,
                "message": f"Silahkan lanjutkan pembayaran menggunakan {payment_method.upper()}."
            })
        
        return jsonify({
            "success": True,
            "message": "Transaksi pembayaran berhasil dibuat.",
            "data": response_data
        }), 201

    except ValueError as e:
        logger.warning(f"Payment request for order {order_id} by UID {uid} failed: {e}")
        status_code = 409 if "status" in str(e) else 400
        return jsonify({"success": False, "message": str(e)}), status_code
    except PermissionError as e:
        logger.warning(f"Access denied for UID {uid} on order {order_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 403
    except RuntimeError as e:
        logger.error(f"Server error creating payment for {order_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

@payments_bp.route('/payments/webhook', methods=['POST'])
def handle_payment_webhook_endpoint():
    """
    Endpoint untuk menerima notifikasi status pembayaran dari gerbang pembayaran.
    Endpoint ini harus selalu merespons dengan cepat dan andal.
    """
    payload = request.get_json()
    if not payload:
        logger.warning("Menerima permintaan webhook kosong.")
        return jsonify({"status": "received", "error": "empty payload"}), 400

    try:
        # Verifikasi signature/hash webhook akan dilakukan di sini di produksi
        # service.verify_webhook_signature(request.headers, request.get_data())
        
        service.process_payment_webhook(payload)
        logger.info(f"Webhook untuk pesanan {payload.get('order_id')} berhasil diproses.")
        # Selalu kembalikan 200 OK jika kita berhasil menerima dan memvalidasi payload,
        # bahkan jika ada kegagalan logika bisnis, untuk mencegah pengiriman ulang dari gerbang pembayaran.
        return jsonify({"status": "received"}), 200
    
    except ValueError as e:
        # Ini terjadi jika payload webhook itu sendiri tidak valid.
        logger.error(f"Webhook tidak valid diterima: {e}")
        return jsonify({"status": "invalid_payload", "message": str(e)}), 400
    except Exception as e:
        # Tangkap semua kesalahan lain untuk memastikan gerbang pembayaran tidak mendapatkan 500
        logger.critical(f"Kesalahan kritis yang tidak tertangani saat memproses webhook: {e}", exc_info=True)
        # Kita tetap mengembalikan 200 agar webhook tidak dikirim ulang tanpa henti,
        # tetapi kita log sebagai CRITICAL agar bisa segera ditindaklanjuti.
        return jsonify({"status": "received_with_error"}), 200
