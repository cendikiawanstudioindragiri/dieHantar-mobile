from __future__ import annotations

from flask import Blueprint, jsonify, current_app

# Register under /api/v1/health
URL_PREFIX = "/api/v1"

bp = Blueprint("health", __name__)


@bp.route("/health", methods=["GET"])
def health():
    version = current_app.config.get("APP_VERSION", "0.0.0")
    return jsonify({"status": "ok", "version": version}), 200
