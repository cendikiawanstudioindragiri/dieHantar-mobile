# blueprints/driver_service.py

from firebase_admin import firestore
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()
DRIVER_COLLECTION = 'drivers'

def get_available_drivers(db):
    """Mengambil daftar dieHantar yang tersedia."""
    try:
        drivers_ref = db.collection(DRIVER_COLLECTION)
        query_stream = drivers_ref.where('is_available', '==', True).stream()
        
        available_drivers = []
        for doc in query_stream:
            driver_data = doc.to_dict()
            driver_data['driver_id'] = doc.id
            available_drivers.append(driver_data)
            
        logger.info(f"Ditemukan {len(available_drivers)} dieHantar tersedia.")
        return available_drivers
    except Exception as e:
        logger.error(f"Gagal mengambil driver yang tersedia: {e}", exc_info=True)
        return []

def assign_order_to_driver(db, order_id, driver_id):
    """Menugaskan pesanan kepada dieHantar dan mengupdate status secara atomis."""
    try:
        batch = db.batch()

        order_ref = db.collection('orders').document(order_id)
        batch.update(order_ref, {
            'driver_id': driver_id,
            'status': 'sedang_diantar',
            'updated_at': firestore.SERVER_TIMESTAMP
        })

        driver_ref = db.collection(DRIVER_COLLECTION).document(driver_id)
        batch.update(driver_ref, {
            'is_available': False
        })

        batch.commit()
        logger.info(f"Pesanan {order_id} berhasil ditugaskan kepada dieHantar {driver_id}.")
        return True
    except Exception as e:
        logger.error(f"Gagal menugaskan pesanan {order_id} ke driver {driver_id}: {e}", exc_info=True)
        return False
