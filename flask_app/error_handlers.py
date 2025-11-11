from __future__ import annotations

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .exceptions import OrderNotFound, InvalidPayment


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(exc: HTTPException):
        payload = {
            "error": {
                "code": exc.code or 500,
                "message": exc.name,
                "detail": exc.description,
            }
        }
        return jsonify(payload), exc.code or 500

    @app.errorhandler(OrderNotFound)
    def handle_order_not_found(exc: OrderNotFound):
        payload = {
            "error": {
                "code": 404,
                "message": "Order not found",
                "detail": getattr(exc, "detail", None),
            }
        }
        return jsonify(payload), 404

    @app.errorhandler(InvalidPayment)
    def handle_invalid_payment(exc: InvalidPayment):
        payload = {
            "error": {
                "code": 422,
                "message": "Invalid payment",
                "detail": getattr(exc, "detail", None),
            }
        }
        return jsonify(payload), 422

    @app.errorhandler(Exception)
    def handle_generic_error(exc: Exception):
        payload = {
            "error": {
                "code": 500,
                "message": "Internal server error",
                "detail": None,
            }
        }
        return jsonify(payload), 500
