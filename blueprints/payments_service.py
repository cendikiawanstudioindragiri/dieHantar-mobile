# blueprints/payments_service.py

from dataclasses import dataclass, asdict
from typing import Dict
import datetime
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger

# Impor layanan yang sudah direfaktor
from .orders_service import get_order_by_id, update_order_status, OrderStatus
from .drivers_service import find_and_assign_nearest_driver # Asumsi fungsi ini akan dibuat

logger = get_logger(__name__)
db = get_firestore_client()

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"

@dataclass
class PaymentTransaction:
    id: str
    order_id: str
    amount: int
    status: PaymentStatus
    redirect_url: str
    created_at: datetime.datetime

# --- Fungsi Layanan Inti ---

def initiate_order_payment(order_id: str, requester_uid: str) -> PaymentTransaction:
    """
    Memvalidasi pesanan dan membuat transaksi pembayaran tiruan.
    Memunculkan exception jika validasi gagal.
    """
    logger.info(f"UID {requester_uid} memulai pembayaran untuk pesanan {order_id}.")
    
    # 1. Dapatkan dan validasi pesanan menggunakan layanan pesanan yang baru
    order = get_order_by_id(order_id)
    
    if order.user_id != requester_uid:
        raise PermissionError("Anda tidak diizinkan membayar pesanan ini.")

    if order.status != OrderStatus.PENDING_PAYMENT.value:
        raise ValueError(f"Pembayaran tidak dapat diproses untuk pesanan dengan status ‘{order.status}’.")

    # 2. Buat transaksi pembayaran tiruan (seperti di layanan lama)
    mock_transaction = _create_mock_charge(order)
    
    # 3. (Opsional) Simpan log transaksi pembayaran ke database
    try:
        db.collection('payment_transactions').document(mock_transaction.id).set(mock_transaction.to_dict())
    except Exception as e:
        logger.error(f"Gagal menyimpan log transaksi pembayaran {mock_transaction.id}: {e}", exc_info=True)
        # Kegagalan ini tidak kritis untuk alur utama, jadi kita hanya log

    return mock_transaction

def process_payment_webhook(payload: Dict):
    """
    Memproses notifikasi webhook dari gerbang pembayaran (tiruan).
    Ini adalah fungsi yang sangat penting yang memicu sisa alur aplikasi.
    """
    logger.info(f"Menerima webhook pembayaran: {payload}")
    order_id = payload.get('order_id')
    transaction_status = payload.get('transaction_status') # e.g., 'settlement', 'expire'

    if not all([order_id, transaction_status]):
        raise ValueError("Webhook payload tidak valid: order_id atau transaction_status tidak ada.")

    try:
        order = get_order_by_id(order_id)
        
        # Hanya proses jika status pembayaran berhasil dan status pesanan masih menunggu
        if transaction_status == 'settlement' and order.status == OrderStatus.PENDING_PAYMENT.value:
            logger.info(f"Pembayaran untuk pesanan {order_id} berhasil. Memperbarui status...")
            
            # 1. Update status pesanan menjadi PROCESSING
            # Layanan pesanan yang baru secara otomatis akan mengirim notifikasi ke pengguna.
            update_order_status(order_id, OrderStatus.PROCESSING)
            
            # 2. Memicu pencarian driver, yang merupakan langkah selanjutnya dalam saga.
            logger.info(f"Memicu pencarian driver untuk pesanan {order_id}.")
            # Di dunia nyata, ini akan menjadi tugas asinkron (misalnya, Celery atau Cloud Tasks).
            # find_and_assign_nearest_driver(order_id, order.delivery_address)
            # Untuk saat ini kita asumsikan fungsi ini ada dan akan kita buat nanti.
            
        elif transaction_status in ['expire', 'cancel', 'deny']:
            logger.warning(f"Pembayaran untuk pesanan {order_id} gagal atau kadaluwarsa. Status: {transaction_status}")
            update_order_status(order_id, OrderStatus.FAILED)
            
    except (ValueError, PermissionError) as e:
        # Dilempar ulang jika get_order_by_id gagal
        logger.error(f"Validasi webhook gagal untuk pesanan {order_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Kesalahan server saat memproses webhook untuk {order_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal memproses notifikasi pembayaran.") from e

# --- Fungsi Helper Internal ---

def _create_mock_charge(order: 'Order') -> PaymentTransaction:
    """Membuat transaksi pembayaran tiruan dan mengembalikan objek PaymentTransaction."""
    transaction_id = f"MOCK-PAY-{order.id[:8]}-{int(datetime.datetime.utcnow().timestamp())}"
    logger.info(f"Membuat charge tiruan {transaction_id} untuk pesanan {order.id}")
    
    # Simulasikan pembaruan pada dokumen pesanan dengan ID transaksi
    order_ref = db.collection('orders').document(order.id)
    order_ref.update({'payment_transaction_id': transaction_id})
    
    return PaymentTransaction(
        id=transaction_id,
        order_id=order.id,
        amount=order.summary.get('total'),
        status=PaymentStatus.PENDING,
        redirect_url=f"https://simulator.example.com/pay/{transaction_id}",
        created_at=datetime.datetime.utcnow()
    )
