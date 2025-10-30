# blueprints/order/__init__.py

from flask import Blueprint, request, jsonify
from ..order_service import (
    calculate_order_summary as calculate_summary_service,
    create_new_order as create_order_service,
    update_order_status as update_status_service,
    cancel_order as cancel_order_service,
    get_user_orders as get_orders_service
)

order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')

@order_bp.route("/calculate-summary", methods=['POST'])
def calculate_order_summary_route():
    data = request.get_json()
    items = data.get('items')
    promotion_code = data.get('promotion_code')
    summary = calculate_summary_service(items, promotion_code)
    return jsonify(summary)

@order_bp.route("/", methods=['POST'])
def create_new_order_route():
    data = request.get_json()
    uid = data.get('uid') # Di dunia nyata, ini akan didapat dari token otentikasi
    order_details = data.get('order_details')
    result = create_order_service(uid, order_details)
    if result["success"]:
        return jsonify(result), 201
    return jsonify(result), 400

@order_bp.route("/<order_id>/status", methods=['PUT'])
def update_order_status_route(order_id):
    data = request.get_json()
    new_status = data.get('new_status')
    result = update_status_service(order_id, new_status)
    if result["success"]:
        return jsonify(result)
    return jsonify(result), 400

@order_bp.route("/<order_id>/cancel", methods=['POST'])
def cancel_order_route(order_id):
    data = request.get_json()
    uid = data.get('uid')
    reason = data.get('reason')
    result = cancel_order_service(order_id, uid, reason)
    if result["success"]:
        return jsonify(result)
    return jsonify(result), 400

@order_bp.route("/history/<uid>/<order_type>", methods=['GET'])
def get_user_orders_route(uid, order_type):
    result = get_orders_service(uid, order_type)
    if result["success"]:
        return jsonify(result["orders"])
    return jsonify(result), 400
