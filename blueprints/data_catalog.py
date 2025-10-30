# blueprints/data_catalog.py

from flask import Blueprint, request, jsonify
from . import data_catalog_service as service

# Definisikan Blueprint untuk katalog data
data_catalog_bp = Blueprint('data_catalog_bp', __name__, url_prefix='/api/v1/catalog')

# --- Rute untuk Dashboard --- #

@data_catalog_bp.route('/home/user/<string:uid>', methods=['GET'])
def get_home_dashboard(uid):
    """Endpoint untuk mendapatkan data utama halaman Home."""
    # TODO: Tambahkan verifikasi token di sini untuk memastikan hanya pengguna
    # yang terotentikasi yang dapat mengakses datanya sendiri.
    result = service.get_home_dashboard_data(uid)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

# --- Rute untuk Lokasi Pengguna --- #

@data_catalog_bp.route('/users/<string:uid>/locations', methods=['GET'])
def get_locations(uid):
    """Endpoint untuk mendapatkan semua lokasi yang disimpan pengguna."""
    # TODO: Amankan endpoint ini dengan verifikasi token.
    result = service.get_user_locations(uid)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

@data_catalog_bp.route('/users/<string:uid>/locations', methods=['POST'])
def add_location(uid):
    """Endpoint untuk menambahkan lokasi baru bagi pengguna."""
    # TODO: Amankan endpoint ini dengan verifikasi token.
    location_data = request.json
    if not location_data:
        return jsonify({"success": False, "message": "Request body tidak boleh kosong."}), 400
        
    result = service.add_user_location(uid, location_data)
    if result["success"]:
        return jsonify(result), 201  # 201 Created
    return jsonify(result), 500

# --- Rute untuk Produk & Pencarian --- #

@data_catalog_bp.route('/products/<string:category>', methods=['GET'])
def get_products(category):
    """Endpoint untuk mendapatkan produk berdasarkan kategori (foods, drinks, services)."""
    limit = request.args.get('limit', 20, type=int)
    result = service.get_products_by_category(category, limit)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 404 if "tidak valid" in result.get("message", "") else 500

@data_catalog_bp.route('/products/search/<string:category>', methods=['GET'])
def search_in_category(category):
    """Endpoint untuk mencari produk dalam sebuah kategori."""
    query = request.args.get('q')
    if not query:
        return jsonify({"success": False, "message": "Parameter query 'q' dibutuhkan."}), 400

    result = service.search_products(category, query)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500

# --- Rute untuk Promosi --- #

@data_catalog_bp.route('/promotions/active', methods=['GET'])
def get_promotions():
    """Endpoint untuk mendapatkan semua promosi yang aktif."""
    result = service.get_active_promotions()
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500
