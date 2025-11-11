from __future__ import annotations

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas.payments import PaymentInitSchema
from ..limiting import limiter

bp = Blueprint("payments", __name__, url_prefix="/api/v1/payments")


@bp.route("/init", methods=["POST"])
@limiter.limit("10/minute")
def init_payment():
    payload = request.get_json(silent=True) or {}
    schema = PaymentInitSchema()
    try:
        data = schema.load(payload)
    except ValidationError as exc:
        return jsonify({"error": "validation_error", "messages": exc.messages}), 422
    # Stub response using validated data
    return jsonify({"status": "initiated", "payment_id": "pay_123", "order_id": data["order_id"]}), 202


@bp.route("/verify", methods=["POST"])
@limiter.limit("30/minute")
def verify_payment():
    payload = request.get_json(silent=True) or {}
    payment_id = payload.get("payment_id")
    if not payment_id:
        return jsonify({"error": "missing_payment_id"}), 400
    # Stub verification
    return jsonify({"status": "verified", "payment_id": payment_id}), 200
