# blueprints/data_catalog_service.py

from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()

FOOD_COLLECTION = 'foods'
PROMOTION_COLLECTION = 'promotions'

def get_all_food_items():
    """Mengambil semua item makanan dari koleksi 'foods'."""
    try:
        food_ref = db.collection(FOOD_COLLECTION)
        all_foods = [doc.to_dict() for doc in food_ref.stream()]
        logger.info(f"Berhasil mengambil {len(all_foods)} item makanan.")
        return {"success": True, "data": all_foods}
    except Exception as e:
        logger.error(f"Gagal mengambil item makanan: {e}", exc_info=True)
        return {"success": False, "message": "Gagal mengambil data makanan."}

def get_all_promotions():
    """Mengambil semua promosi dari koleksi 'promotions'."""
    try:
        promo_ref = db.collection(PROMOTION_COLLECTION)
        all_promotions = [doc.to_dict() for doc in promo_ref.stream()]
        logger.info(f"Berhasil mengambil {len(all_promotions)} promosi.")
        return {"success": True, "data": all_promotions}
    except Exception as e:
        logger.error(f"Gagal mengambil promosi: {e}", exc_info=True)
        return {"success": False, "message": "Gagal mengambil data promosi."}
