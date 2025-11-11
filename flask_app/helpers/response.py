from __future__ import annotations

from flask import jsonify


def success(data=None, message: str | None = None, status_code: int = 200):
    payload = {"success": True, "message": message, "data": data}
    return jsonify(payload), status_code


def error(code: int, message: str, detail: str | None = None):
    payload = {"error": {"code": code, "message": message, "detail": detail}}
    return jsonify(payload), code
