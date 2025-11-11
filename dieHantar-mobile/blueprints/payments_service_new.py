# blueprints/payments_service_new.py

from dataclasses import dataclass, asdict
from typing import Dict, Optional, List
import datetime
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger

# Import layanan yang sudah direfaktor
from .orders_service import get_order_by_id, update_order_status, OrderStatus
from .drivers_service import find_and_assign_nearest_driver
from . import midtrans_service as midtrans

logger = get_logger(__name__)
db = get_firestore_client()

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

@dataclass
class PaymentTransaction:
    id: str
    order_id: str
    amount: int
    status: PaymentStatus
    payment_method: Optional[str] = None
    redirect_url: Optional[str] = None
    snap_token: Optional[str] = None
    transaction_id: Optional[str] = None  # Midtrans transaction ID
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        # Convert enum to string
        if isinstance(data.get('status'), PaymentStatus):
            data['status'] = data['status'].value
        # Convert datetime to ISO string
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
        return data

# --- Fungsi Layanan Inti ---

def initiate_order_payment(order_id: str, requester_uid: str, 
                          payment_method: str = "snap") -> PaymentTransaction:
    """
    Memvalidasi pesanan dan membuat transaksi pembayaran menggunakan Midtrans.
    
    Args:
        order_id: ID pesanan
        requester_uid: UID user yang request payment
        payment_method: Method pembayaran (snap, gopay, bca_va, etc.)
    
    Returns:
        PaymentTransaction: Object transaksi pembayaran
    """
    logger.info(f"UID {requester_uid} memulai pembayaran untuk pesanan {order_id} via {payment_method}.")
    
    # 1. Dapatkan dan validasi pesanan
    order = get_order_by_id(order_id)
    
    if order.user_id != requester_uid:
        raise PermissionError("Anda tidak diizinkan membayar pesanan ini.")

    if order.status != OrderStatus.PENDING_PAYMENT.value:
        raise ValueError(f"Pembayaran tidak dapat diproses untuk pesanan dengan status '{order.status}'.")

    try:
        # 2. Siapkan data untuk Midtrans
        payment_items = []
        for item in order.items:
            payment_items.append(midtrans.PaymentItem(
                id=item.get('id', 'unknown'),
                price=item.get('price', 0),
                quantity=item.get('quantity', 1),
                name=item.get('name', 'Unknown Item'),
                category="food_delivery"
            ))

        # 3. Siapkan customer info
        customer_info = midtrans.CustomerInfo(
            first_name=order.user_info.get('first_name', 'Customer'),
            last_name=order.user_info.get('last_name', ''),
            email=order.user_info.get('email', f"user-{requester_uid}@diehantar.com"),
            phone=order.user_info.get('phone', '+62812345678'),
            shipping_address={
                "first_name": order.user_info.get('first_name', 'Customer'),
                "last_name": order.user_info.get('last_name', ''),
                "address": order.delivery_address.get('address', ''),
                "city": order.delivery_address.get('city', ''),
                "postal_code": order.delivery_address.get('postal_code', ''),
                "country_code": "IDN"
            }
        )

        # 4. Generate unique order ID untuk Midtrans
        midtrans_order_id = midtrans.generate_order_id(f"DH-{order_id}")
        
        # 5. Buat payment berdasarkan method
        payment_response = None
        
        if payment_method == "snap":
            # Snap payment (support multiple payment methods)
            snap_response = midtrans.create_snap_payment(
                order_id=midtrans_order_id,
                gross_amount=order.summary.get('total', 0),
                items=payment_items,
                customer=customer_info,
                custom_expiry={
                    "start_time": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S +0700"),
                    "unit": "minutes",
                    "duration": 60  # 1 hour expiry
                }
            )
            
            payment_response = {
                "snap_token": snap_response.get("token"),
                "redirect_url": snap_response.get("redirect_url"),
                "payment_method": "snap"
            }
            
        else:
            # Direct payment method
            direct_payment = midtrans.create_direct_payment(
                order_id=midtrans_order_id,
                gross_amount=order.summary.get('total', 0),
                items=payment_items,
                customer=customer_info,
                payment_method=payment_method
            )
            
            payment_response = {
                "transaction_id": direct_payment.transaction_id,
                "payment_url": direct_payment.payment_url,
                "va_number": direct_payment.va_number,
                "qr_code": direct_payment.qr_code,
                "deeplink_redirect_url": direct_payment.deeplink_redirect_url,
                "payment_method": payment_method
            }

        # 6. Buat PaymentTransaction object
        payment_transaction = PaymentTransaction(
            id=f"pay-{order_id}-{int(datetime.datetime.utcnow().timestamp())}",
            order_id=order_id,
            amount=order.summary.get('total', 0),
            status=PaymentStatus.PENDING,
            payment_method=payment_method,
            redirect_url=payment_response.get("redirect_url") or payment_response.get("payment_url"),
            snap_token=payment_response.get("snap_token"),
            transaction_id=midtrans_order_id,
            created_at=datetime.datetime.utcnow()
        )

        # 7. Simpan record pembayaran
        payment_ref = db.collection('payment_transactions').document(payment_transaction.id)
        payment_ref.set(payment_transaction.to_dict())

        # 8. Update order dengan payment transaction ID
        order_ref = db.collection('orders').document(order_id)
        order_ref.update({
            'payment_transaction_id': payment_transaction.id,
            'midtrans_order_id': midtrans_order_id,
            'updated_at': datetime.datetime.utcnow()
        })

        logger.info(f"Payment transaction {payment_transaction.id} created for order {order_id}")
        return payment_transaction
        
    except Exception as e:
        logger.error(f"Error creating payment for order {order_id}: {e}", exc_info=True)
        raise RuntimeError(f"Gagal membuat transaksi pembayaran: {str(e)}") from e

def process_payment_webhook(payload: Dict) -> bool:
    """
    Process webhook notification dari Midtrans.
    Delegasi ke midtrans_service untuk handling yang lebih specific.
    """
    try:
        return midtrans.process_webhook_notification(payload)
    except Exception as e:
        logger.error(f"Error processing payment webhook: {e}", exc_info=True)
        return False

def get_payment_methods() -> List[Dict]:
    """
    Dapatkan daftar payment methods yang tersedia.
    
    Returns:
        List[Dict]: Daftar payment methods
    """
    return [
        {
            "id": "snap",
            "name": "Snap Payment",
            "description": "All payment methods (Credit Card, E-wallet, Bank Transfer)",
            "icon": "snap_icon.png"
        },
        {
            "id": "gopay",
            "name": "GoPay",
            "description": "Pembayaran menggunakan GoPay",
            "icon": "gopay_icon.png"
        },
        {
            "id": "shopeepay", 
            "name": "ShopeePay",
            "description": "Pembayaran menggunakan ShopeePay",
            "icon": "shopeepay_icon.png"
        },
        {
            "id": "bca_va",
            "name": "BCA Virtual Account",
            "description": "Transfer melalui Virtual Account BCA",
            "icon": "bca_icon.png"
        },
        {
            "id": "bni_va",
            "name": "BNI Virtual Account", 
            "description": "Transfer melalui Virtual Account BNI",
            "icon": "bni_icon.png"
        },
        {
            "id": "bri_va",
            "name": "BRI Virtual Account",
            "description": "Transfer melalui Virtual Account BRI", 
            "icon": "bri_icon.png"
        }
    ]