from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("chats", __name__, url_prefix="/api/v1/chats")


@bp.route("/handshake", methods=["GET"])
def handshake():
    # Placeholder for future WebSocket setup (Flask-SocketIO)
    return jsonify({"status": "ok", "message": "websocket placeholder"}), 200
