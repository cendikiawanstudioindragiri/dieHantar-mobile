# blueprints/data_catalog/__init__.py

from flask import Blueprint, jsonify
from ..data_catalog_service import get_all_food_items, get_all_promotions

data_catalog_bp = Blueprint('data_catalog_bp', __name__)

@data_catalog_bp.route("/foods", methods=['GET'])
def get_foods_route():
    result = get_all_food_items()
    if result["success"]:
        return jsonify(result["data"])
    return jsonify({"error": result["message"]}), 500

@data_catalog_bp.route("/promotions", methods=['GET'])
def get_promotions_route():
    result = get_all_promotions()
    if result["success"]:
        return jsonify(result["data"])
    return jsonify({"error": result["message"]}), 500
