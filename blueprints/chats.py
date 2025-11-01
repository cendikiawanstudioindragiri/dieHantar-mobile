# blueprints/chats.py

from flask import Blueprint, request, jsonify
from logger_config import get_logger
from .auth_service import token_required
from . import chats_service as service

# URL prefix tetap di /api/v1/orders karena chat terikat pada pesanan
chats_bp = Blueprint('chats', __name__, url_prefix='/api/v1/orders')
logger = get_logger('ChatsBlueprint')

@chats_bp.route('/<string:order_id>/chat', methods=['POST'])
@token_required
def send_message_endpoint(uid, order_id):
    """Endpoint aman untuk mengirim pesan baru dalam sebuah pesanan."""
    data = request.get_json()
    if not data or not data.get('text'):
        return jsonify({"success": False, "message": "Teks pesan tidak boleh kosong."}), 400

    try:
        message = service.send_message(
            order_id=order_id,
            sender_id=uid, # UID dari token yang terotentikasi
            text=data.get('text')
        )
        logger.info(f"Pesan baru {message.id} dalam pesanan {order_id} berhasil dikirim oleh UID {uid}.")
        return jsonify({"success": True, "message": "Pesan berhasil dikirim.", "chat_message": message.to_dict()}), 201

    except ValueError as e:
        logger.warning(f"Pengiriman pesan oleh UID {uid} ke pesanan {order_id} gagal: {e}")
        # Bisa 400 (Bad Request) atau 404 (Not Found) tergantung pesan error
        status_code = 404 if "tidak ditemukan" in str(e) else 400
        return jsonify({"success": False, "message": str(e)}), status_code
    except PermissionError as e:
        logger.warning(f"Akses ditolak untuk UID {uid} mengirim pesan ke pesanan {order_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 403
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} mengirim pesan ke pesanan {order_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500

@chats_bp.route('/<string:order_id>/chat', methods=['GET'])
@token_required
def get_chat_history_endpoint(uid, order_id):
    """Endpoint aman untuk mengambil riwayat obrolan dari sebuah pesanan."""
    try:
        history = service.get_chat_history(order_id=order_id, requester_id=uid)
        logger.info(f"UID {uid} berhasil mengambil riwayat chat untuk pesanan {order_id}.")
        # Ubah setiap objek ChatMessage menjadi dict
        history_dicts = [msg.to_dict() for msg in history]
        return jsonify({"success": True, "history": history_dicts}), 200

    except ValueError as e:
        logger.warning(f"Pengambilan chat oleh UID {uid} pada pesanan {order_id} gagal: {e}")
        return jsonify({"success": False, "message": str(e)}), 404
    except PermissionError as e:
        logger.warning(f"Akses ditolak untuk UID {uid} mengambil chat pesanan {order_id}: {e}")
        return jsonify({"success": False, "message": str(e)}), 403
    except RuntimeError as e:
        logger.error(f"Kesalahan server saat UID {uid} mengambil chat pesanan {order_id}: {e}", exc_info=True)
        return jsonify({"success": False, "message": str(e)}), 500
