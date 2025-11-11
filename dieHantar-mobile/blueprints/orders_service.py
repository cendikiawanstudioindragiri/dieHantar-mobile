# blueprints/orders_service.py

from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict
import datetime
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()
ORDERS_COLLECTION = 'orders'

class OrderStatus(Enum):
    PENDING = "pending"           # Pesanan dibuat, menunggu konfirmasi/pembayaran
    CONFIRMED = "confirmed"       # Pembayaran berhasil, menunggu driver
    PREPARING = "preparing"       # Merchant sedang menyiapkan pesanan
    AWAITING_DRIVER = "awaiting_driver"
    IN_DELIVERY = "in_delivery"   # Driver sedang dalam perjalanan mengantar
    DELIVERED = "delivered"       # Pesanan telah sampai di tujuan
    CANCELLED = "cancelled"       # Pesanan dibatalkan

@dataclass
class OrderItem:
    food_id: str
    quantity: int
    price_per_item: float

@dataclass
class Order:
    id: str
    user_id: str
    items: List[OrderItem]
    status: str
    total_price: float
    delivery_address: Dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    driver_id: Optional[str] = None
    promotion_code: Optional[str] = None

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'Order':
        items = [OrderItem(**item) for item in data.get('items', [])]
        return Order(
            id=doc_id,
            user_id=data.get('user_id'),
            items=items,
            status=data.get('status', OrderStatus.PENDING.value),
            total_price=data.get('total_price'),
            delivery_address=data.get('delivery_address'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            driver_id=data.get('driver_id'),
            promotion_code=data.get('promotion_code')
        )

    def to_dict(self) -> dict:
        return asdict(self)

def create_new_order(user_id: str, items_data: List[Dict], address: Dict, promo_code: Optional[str]) -> Order:
    if not items_data or not address:
        raise ValueError("Item pesanan dan alamat pengiriman diperlukan.")

    total_price = sum(item['quantity'] * item['price_per_item'] for item in items_data)
    # Di sini bisa ditambahkan logika diskon dari promo_code

    order_data = {
        "user_id": user_id,
        "items": items_data,
        "status": OrderStatus.PENDING.value,
        "total_price": total_price,
        "delivery_address": address,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
        "driver_id": None,
        "promotion_code": promo_code
    }
    try:
        order_ref = db.collection(ORDERS_COLLECTION).document()
        order_ref.set(order_data)
        logger.info(f"Pesanan baru {order_ref.id} berhasil dibuat oleh UID {user_id}")
        return Order.from_dict(order_ref.id, order_data)
    except Exception as e:
        logger.error(f"Gagal menyimpan pesanan baru untuk UID {user_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal menyimpan pesanan baru ke database.") from e

def get_order_for_user(order_id: str, user_id: str) -> Order:
    try:
        order_ref = db.collection(ORDERS_COLLECTION).document(order_id)
        doc = order_ref.get()
        if not doc.exists:
            raise ValueError(f"Pesanan dengan ID {order_id} tidak ditemukan.")
        
        order_data = doc.to_dict()
        if order_data.get('user_id') != user_id:
            logger.warning(f"UID {user_id} mencoba mengakses pesanan {order_id} milik orang lain.")
            raise PermissionError("Anda tidak diizinkan untuk melihat pesanan ini.")
        
        return Order.from_dict(doc.id, order_data)
    except (ValueError, PermissionError):
        raise
    except Exception as e:
        logger.error(f"Gagal mengambil pesanan {order_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal mengambil data pesanan dari database.") from e
