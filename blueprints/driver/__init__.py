# blueprints/driver/__init__.py

from flask import Blueprint, jsonify
from ..driver_service import get_available_drivers

driver_bp = Blueprint('driver_bp', __name__, url_prefix='/drivers')

@driver_bp.route("/available", methods=['GET'])
def get_available_drivers_route():
    drivers = get_available_drivers()
    return jsonify(drivers)
