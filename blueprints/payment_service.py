# blueprints/payment_service.py

from firebase_admin import firestore
from firebase_config import get_firestore_client
from .order_service import update_order_status, ORDER_STATUSES
from logger_config import get_logger
from typing import Dict, Any

# Inisialisasi Logger
logger = get_logger('PaymentService')

# Inisialisasi Klien Firestore
db = get_firestore_client()

PAYMENT_METHODS_COLLECTION = 'user_payment_methods'
REVIEW_COLLECTION = 'reviews'

# --- I. Manajemen Metode Pembayaran (S. Payment Methods) ---

def add_new_payment_method(uid: str, card_data: Dict[str, Any]) -> dict:
    """
    Menyimpan token kartu (bukan detail kartu mentah) yang aman dari Payment Gateway.
    PENTING: Data kartu sensitif (nomor, CVV) TIDAK PERNAH boleh disimpan langsung.
    """
    try:
        collection_ref = db.collection('artifacts').document('diehantar-app').collection('users').document(uid).collection(PAYMENT_METHODS_COLLECTION)
        
        # Cek apakah ini metode pertama untuk dijadikan default
        is_default = not any(collection_ref.limit(1).stream())
        
        data_to_save = {
            "token_id": card_data['token'],
            "last_digits": card_data['last4'],
            "brand": card_data['brand'],
            "type": card_data.get('type', 'credit_card'),
            "is_default": is_default,
            "created_at": firestore.SERVER_TIMESTAMP,
        }
        
        doc_ref = collection_ref.document()
        doc_ref.set(data_to_save)
        logger.info(f"Metode pembayaran baru (token) ditambahkan untuk UID {uid}: {doc_ref.id}")
        
        return {"success": True, "method_id": doc_ref.id, "message": "Metode pembayaran berhasil ditambahkan."}
    except Exception as e:
        logger.error(f"Gagal menambahkan metode pembayaran UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat tokenisasi pembayaran."}

def handle_payment_webhook(webhook_payload: Dict[str, Any]) -> dict:
    """
    Menangani notifikasi balik (Webhook) dari Payment Gateway.
    """
    order_id = webhook_payload.get('reference_id') 
    status = webhook_payload.get('transaction_status') 

    if status in ['success', 'settlement']:
        logger.info(f"WEBHOOK: Pembayaran sukses untuk Order {order_id}. Memperbarui status.")
        result = update_order_status(order_id, ORDER_STATUSES['PROCESSING'])
        
        if result['success']:
            return {"success": True, "message": "Status pesanan diperbarui."}
        else:
            logger.error(f"Gagal memperbarui status order {order_id} meskipun pembayaran sukses.")
            return {"success": False, "message": "Pembayaran sukses tetapi gagal memperbarui order."}

    elif status in ['failure', 'expire', 'cancel']:
        logger.warning(f"WEBHOOK: Pembayaran gagal untuk Order {order_id}. Status: {status}.")
        update_order_status(order_id, ORDER_STATUSES['CANCELED'], reason=f"Pembayaran gagal: {status}")
        return {"success": True, "message": "Pesanan dibatalkan karena pembayaran gagal."}

    else:
        return {"success": True, "message": "Status tidak relevan, diabaikan."}

# --- II. Rating dan Review (U. Delivery successful + rating + review) ---

def submit_order_rating_review(uid: str, order_id: str, rating_data: Dict[str, Any]) -> dict:
    """
    Mengirimkan rating dan review untuk Order.
    """
    try:
        review_id = f"{order_id}_{uid}"
        
        data_to_save = {
            "order_id": order_id,
            "user_id": uid,
            "driver_rating": rating_data.get('driver_rating'),
            "driver_review": rating_data.get('driver_review'),
            "meal_rating": rating_data.get('meal_rating'),
            "meal_review": rating_data.get('meal_review'),
            "timestamp": firestore.SERVER_TIMESTAMP,
            "has_thanks_given": rating_data.get('has_thanks_given', False)
        }
        
        db.collection(REVIEW_COLLECTION).document(review_id).set(data_to_save, merge=True)
        
        logger.info(f"Rating dan Review untuk Order {order_id} berhasil disimpan.")
        return {"success": True, "message": "Terima kasih atas penilaian Anda!"}
    except Exception as e:
        logger.error(f"Gagal menyimpan rating Order {order_id}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat menyimpan penilaian."}

# --- III. Fitur PEMBERIAN TERIMA KASIH (U. Give Thanks) ---

def give_thanks_to_driver(driver_id: str, amount: int) -> dict:
    """
    Memberikan tip/ucapan terima kasih kepada driver.
    """
    try:
        driver_tip_ref = db.collection('driver_tips').document(driver_id)
        driver_tip_ref.update({
            "total_tips": firestore.Increment(amount),
            "last_tip_at": firestore.SERVER_TIMESTAMP
        })
        
        logger.info(f"Driver {driver_id} menerima tip sebesar {amount}.")
        return {"success": True, "message": f"Terima kasih Anda sebesar Rp {amount} berhasil dikirimkan ke Driver."}
    except Exception as e:
        logger.error(f"Gagal memberikan tip ke Driver {driver_id}: {e}", exc_info=True)
        return {"success": False, "message": "Gagal memproses tip."}