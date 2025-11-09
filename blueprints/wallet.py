# blueprints/wallet.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required

# Blueprint untuk wallet/dompet digital
wallet_bp = Blueprint('wallet', __name__, url_prefix='/api/v1/wallet')
logger = get_logger('WalletBlueprint')

@wallet_bp.route('/balance', methods=['GET'])
@token_required
def get_balance(uid):
    """Endpoint untuk mendapatkan saldo wallet pengguna."""
    try:
        # Stub implementation - returns placeholder balance
        balance_data = {
            "user_id": uid,
            "balance": 0.0,
            "currency": "IDR"
        }
        logger.info(f"Berhasil mengambil saldo wallet untuk UID {uid}.")
        return jsonify({"success": True, "data": balance_data}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil saldo wallet untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@wallet_bp.route('/transactions', methods=['GET'])
@token_required
def get_transactions(uid):
    """Endpoint untuk mendapatkan riwayat transaksi wallet."""
    try:
        # Stub implementation - returns empty transaction list
        transactions_data = {
            "user_id": uid,
            "transactions": []
        }
        logger.info(f"Berhasil mengambil transaksi wallet untuk UID {uid}.")
        return jsonify({"success": True, "data": transactions_data}), 200
    except Exception as e:
        logger.error(f"Gagal mengambil transaksi wallet untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@wallet_bp.route('/topup', methods=['POST'])
@token_required
def topup_wallet(uid):
    """Endpoint untuk top-up saldo wallet (placeholder)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        amount = data.get('amount', 0)
        if amount <= 0:
            return jsonify({"success": False, "message": "Jumlah top-up harus lebih dari 0."}), 400

        # Stub implementation - placeholder for future functionality
        logger.info(f"UID {uid} mencoba top-up wallet sebesar {amount}.")
        return jsonify({
            "success": True,
            "message": "Top-up berhasil diproses (placeholder).",
            "data": {
                "transaction_id": "topup_placeholder_id",
                "amount": amount,
                "user_id": uid
            }
        }), 201
    except Exception as e:
        logger.error(f"Gagal memproses top-up untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500

@wallet_bp.route('/withdraw', methods=['POST'])
@token_required
def withdraw_wallet(uid):
    """Endpoint untuk penarikan saldo wallet (placeholder)."""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400

    try:
        amount = data.get('amount', 0)
        if amount <= 0:
            return jsonify({"success": False, "message": "Jumlah penarikan harus lebih dari 0."}), 400

        # Stub implementation - placeholder for future functionality
        logger.info(f"UID {uid} mencoba penarikan wallet sebesar {amount}.")
        return jsonify({
            "success": True,
            "message": "Penarikan berhasil diproses (placeholder).",
            "data": {
                "transaction_id": "withdraw_placeholder_id",
                "amount": amount,
                "user_id": uid
            }
        }), 201
    except Exception as e:
        logger.error(f"Gagal memproses penarikan untuk UID {uid}: {e}", exc_info=True)
        return jsonify({"success": False, "message": "Terjadi kesalahan pada server."}), 500
