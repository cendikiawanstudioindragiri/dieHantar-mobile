# blueprints/order_service.py

from firebase_admin import firestore
from firebase_config import get_firestore_client
from logger_config import get_logger
from typing import List, Dict, Any
import uuid

# Inisialisasi Logger
logger = get_logger('OrderService')

# Inisialisasi Klien Firestore
db = get_firestore_client()

ORDER_COLLECTION = 'orders'
MAX_DRIVER_DISTANCE_KM = 5 # Jarak maksimal driver yang dicari

# Status Pesanan (Q. Order Tracking)
ORDER_STATUSES = {
    'PENDING_PAYMENT': 'Menunggu Pembayaran',
    'PROCESSING': 'Pesanan Diproses',
    'DRIVER_SEARCHING': 'Mencari Driver',
    'DRIVER_EN_ROUTE': 'Driver Menuju Lokasi Ambil',
    'PICKED_UP': 'Pesanan Diambil Driver',
    'DELIVERING': 'Driver Menuju Lokasi Anda',
    'DELIVERED': 'Pesanan Berhasil Dikirim', # U. Delivery successful
    'CANCELED': 'Pesanan Dibatalkan', # T. Cancel order
    'REFUNDED': 'Dana Dikembalikan',
}

# --- I. Pembuatan dan Perhitungan Pesanan (O. My Basket) ---

def calculate_order_summary(items: List[Dict[str, Any]], promotion_code: str = None) -> dict:
    """
    Menghitung subtotal, biaya pengiriman, diskon, dan total akhir pesanan.
    Fungsi ini harus dipanggil di sisi server untuk mencegah kecurangan.

    Args:
        items (List[Dict]): Daftar item di keranjang (e.g., [{'id': 'f1', 'price': 50000, 'qty': 1, 'category': 'foods'}, ...]).
        promotion_code (str): Kode promosi yang dipilih (P. promotions_selected).
    """
    subtotal = sum(item['price'] * item['qty'] for item in items)
    shipping_cost = 15000  # Biaya pengiriman tetap (Contoh)
    discount_amount = 0
    promotion_details = None

    if promotion_code:
        # Lakukan panggilan ke Firestore untuk memverifikasi kode promosi
        promo_ref = db.collection('promotions').document(promotion_code).get()
        if promo_ref.exists:
            promo_data = promo_ref.to_dict()
            promotion_details = promo_data
            
            # Logika diskon sederhana (Contoh: Diskon 10% maksimum 25.000)
            if promo_data.get('type') == 'PERCENTAGE':
                max_disc = promo_data.get('max_discount', 25000)
                percentage = promo_data.get('value', 0.1)
                discount_amount = min(subtotal * percentage, max_disc)

    total_amount = subtotal + shipping_cost - discount_amount

    return {
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "discount_amount": discount_amount,
        "promotion_details": promotion_details,
        "total_amount": max(total_amount, 0), # Total tidak boleh negatif
        "is_valid": total_amount >= 0
    }

def create_new_order(uid: str, order_details: Dict[str, Any]) -> dict:
    """
    Membuat dokumen pesanan baru setelah perhitungan dan sebelum pembayaran.

    Args:
        uid (str): ID pengguna.
        order_details (Dict): Detail pesanan termasuk items, alamat, payment_method.
    """
    try:
        summary = calculate_order_summary(order_details['items'], order_details.get('promotion_code'))
        
        if not summary['is_valid']:
            return {"success": False, "message": "Perhitungan pesanan tidak valid."}
        
        order_id = str(uuid.uuid4())[:8].upper() # Contoh format Order ID
        
        new_order = {
            "order_id": order_id,
            "user_id": uid,
            "items": order_details['items'],
            "summary": summary,
            "delivery_address": order_details['delivery_address'],
            "payment_method": order_details['payment_method'],
            "status": ORDER_STATUSES['PENDING_PAYMENT'],
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "driver_info": None,
            "tracking_history": [
                {"timestamp": firestore.SERVER_TIMESTAMP, "status": ORDER_STATUSES['PENDING_PAYMENT']}
            ]
        }

        db.collection(ORDER_COLLECTION).document(order_id).set(new_order)
        logger.info(f"Pesanan baru {order_id} dibuat oleh UID {uid}.")

        return {"success": True, "order_id": order_id, "total_amount": summary['total_amount'], "message": "Pesanan berhasil dibuat. Lanjutkan ke pembayaran."}
    except Exception as e:
        logger.error(f"Gagal membuat pesanan baru untuk UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat membuat pesanan."}


# --- II. Manajemen Status dan Pembatalan (Q, T) ---

def update_order_status(order_id: str, new_status: str, uid: str = None, driver_id: str = None) -> dict:
    """
    Memperbarui status pesanan (Q. Order Tracking step 1-4).
    """
    if new_status not in ORDER_STATUSES.values():
        return {"success": False, "message": "Status pesanan tidak valid."}
        
    try:
        order_ref = db.collection(ORDER_COLLECTION).document(order_id)
        
        update_data = {
            "status": new_status,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "tracking_history": firestore.ArrayUnion([
                {"timestamp": firestore.SERVER_TIMESTAMP, "status": new_status}
            ])
        }

        # Jika status terkait driver, tambahkan info driver (R. Driver information)
        if driver_id:
            update_data['driver_info'] = {"driver_id": driver_id, "assigned_at": firestore.SERVER_TIMESTAMP}
            
        order_ref.update(update_data)
        logger.info(f"Status pesanan {order_id} diubah menjadi: {new_status}")
        
        # PENTING: Panggil fungsi notifikasi setelah status berhasil diubah
        # send_fcm_notification(uid_token, "Status Pesanan", f"Pesanan Anda kini: {new_status}")

        return {"success": True, "new_status": new_status, "message": f"Status pesanan berhasil diubah ke {new_status}."}
    except Exception as e:
        logger.error(f"Gagal memperbarui status pesanan {order_id}: {e}", exc_info=True)
        return {"success": False, "message": "Gagal memperbarui status pesanan."}

def cancel_order(order_id: str, uid: str, reason: str) -> dict:
    """
    Membatalkan pesanan yang belum diproses atau belum diambil (T. Cancel order).
    """
    try:
        order_doc = db.collection(ORDER_COLLECTION).document(order_id).get()
        if not order_doc.exists:
            return {"success": False, "message": "Pesanan tidak ditemukan."}
            
        order_data = order_doc.to_dict()
        
        # Hanya bisa dibatalkan jika statusnya masih PENDING_PAYMENT atau PROCESSING
        if order_data['status'] not in [ORDER_STATUSES['PENDING_PAYMENT'], ORDER_STATUSES['PROCESSING']]:
            return {"success": False, "message": f"Pesanan tidak bisa dibatalkan pada status {order_data['status']}."}

        # Update status pembatalan
        db.collection(ORDER_COLLECTION).document(order_id).update({
            "status": ORDER_STATUSES['CANCELED'],
            "cancellation_reason": reason,
            "updated_at": firestore.SERVER_TIMESTAMP,
            "tracking_history": firestore.ArrayUnion([
                {"timestamp": firestore.SERVER_TIMESTAMP, "status": ORDER_STATUSES['CANCELED'], "reason": reason}
            ])
        })
        
        logger.info(f"Pesanan {order_id} dibatalkan oleh UID {uid} dengan alasan: {reason}")
        
        # PENTING: Jika pembayaran sudah dilakukan, picu fungsi Refund di payment_service.py
        
        return {"success": True, "message": "Pesanan berhasil dibatalkan. Dana akan diproses pengembaliannya (jika berlaku)."}
    except Exception as e:
        logger.error(f"Gagal membatalkan pesanan {order_id}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat membatalkan pesanan."}


# --- III. Riwayat Pesanan (V. Orders) ---

def get_user_orders(uid: str, order_type: str) -> dict:
    """
    Mengambil riwayat pesanan pengguna (V. Orders).

    Args:
        uid (str): ID pengguna.
        order_type (str): 'active', 'completed', atau 'canceled'.
    """
    order_type = order_type.lower()
    
    # Menentukan status yang akan dicari berdasarkan tipe
    status_filter = {
        'active': [ORDER_STATUSES['PROCESSING'], ORDER_STATUSES['DRIVER_SEARCHING'], ORDER_STATUSES['DRIVER_EN_ROUTE'], ORDER_STATUSES['PICKED_UP'], ORDER_STATUSES['DELIVERING']],
        'completed': [ORDER_STATUSES['DELIVERED']],
        'canceled': [ORDER_STATUSES['CANCELED'], ORDER_STATUSES['REFUNDED']]
    }.get(order_type)
    
    if not status_filter:
        return {"success": False, "message": "Tipe pesanan tidak valid."}
        
    try:
        # Query Firestore untuk pesanan milik user ini dengan status yang relevan
        query = db.collection(ORDER_COLLECTION)\
            .where('user_id', '==', uid)\
            .where('status', 'in', status_filter)\
            .order_by('created_at', direction=firestore.Query.DESCENDING)
            
        orders = [doc.to_dict() for doc in query.stream()]
        
        if not orders and order_type in ['active', 'canceled']:
             # V. order_Not found
             return {"success": True, "orders": [], "message": "Tidak ada pesanan ditemukan."}
             
        logger.info(f"Berhasil mengambil {len(orders)} pesanan tipe {order_type} untuk UID {uid}.")
        return {"success": True, "orders": orders}
    except Exception as e:
        logger.error(f"Gagal mengambil pesanan tipe {order_type} untuk UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat mengambil riwayat pesanan."}