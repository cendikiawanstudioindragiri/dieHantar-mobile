from __future__ import annotations

from functools import wraps
from typing import Callable, Any

from flask import Blueprint, request, jsonify, current_app
from ..limiting import limiter

try:  # Optional dependency; only needed if this blueprint is used
    from firebase_admin import auth as fb_auth  # type: ignore
except Exception:  # pragma: no cover - avoid hard fail if not installed
    fb_auth = None  # type: ignore


bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")


def require_auth(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        if fb_auth is None:
            return jsonify({"error": "firebase_not_configured"}), 501

        id_header = request.headers.get("Authorization", "")
        if not id_header:
            return jsonify({"error": "missing_authorization"}), 401
        token = id_header
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        try:
            decoded = fb_auth.verify_id_token(token)
        except Exception:
            return jsonify({"error": "invalid_token"}), 401

        # Attach user to request context via flask.g to avoid mutating request
        from flask import g

        g.user = decoded
        return f(*args, **kwargs)

    return wrapper


@bp.route("/health", methods=["GET"])
def auth_health():
    return jsonify({"status": "ok", "component": "auth"}), 200


@bp.route("/me", methods=["GET"])
@limiter.limit(lambda: current_app.config.get("RATE_LIMIT_AUTH", "5/minute"))
@require_auth
def me():
    from flask import g

    user = getattr(g, "user", {}) or {}
    return (
        jsonify({"uid": user.get("uid"), "email": user.get("email")}),
        200,
    )
