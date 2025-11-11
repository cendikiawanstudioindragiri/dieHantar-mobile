# blueprints/midtrans_service.py

import os
import hmac
import hashlib
import json
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Optional, List
from enum import Enum
import midtransclient
import requests
from logger_config import get_logger
from firebase_config import get_firestore_client

logger = get_logger(__name__)
db = get_firestore_client()

# Midtrans Configuration
MIDTRANS_IS_PRODUCTION = os.getenv('MIDTRANS_IS_PRODUCTION', 'false').lower() == 'true'
MIDTRANS_SERVER_KEY = os.getenv('MIDTRANS_SERVER_KEY')
MIDTRANS_CLIENT_KEY = os.getenv('MIDTRANS_CLIENT_KEY')

if not MIDTRANS_SERVER_KEY:
    logger.warning("MIDTRANS_SERVER_KEY tidak ditemukan. Payment service akan menggunakan mode mock.")
    MIDTRANS_SERVER_KEY = "mock_server_key"

# Initialize Midtrans clients
try:
    snap = midtransclient.Snap(
        is_production=MIDTRANS_IS_PRODUCTION,
        server_key=MIDTRANS_SERVER_KEY,
        client_key=MIDTRANS_CLIENT_KEY
    )
    core_api = midtransclient.CoreApi(
        is_production=MIDTRANS_IS_PRODUCTION,
        server_key=MIDTRANS_SERVER_KEY,
        client_key=MIDTRANS_CLIENT_KEY
    )
    logger.info(f"Midtrans initialized: Production={MIDTRANS_IS_PRODUCTION}")
except Exception as e:
    logger.error(f"Failed to initialize Midtrans: {e}")
    snap = None
    core_api = None

class PaymentMethod(Enum):
    SNAP = "snap"              # Snap payment (all methods)
    GOPAY = "gopay"            # GoPay
    SHOPEEPAY = "shopeepay"    # ShopeePay  
    OVO = "ovo"                # OVO
    DANA = "dana"              # DANA
    BCA_VA = "bca_va"          # BCA Virtual Account
    BNI_VA = "bni_va"          # BNI Virtual Account
    BRI_VA = "bri_va"          # BRI Virtual Account
    PERMATA_VA = "permata_va"  # Permata Virtual Account
    CREDIT_CARD = "credit_card" # Credit Card
    BANK_TRANSFER = "bank_transfer" # Bank Transfer

class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "settlement"
    FAILED = "failure"
    CANCELLED = "cancel"
    EXPIRED = "expire"
    REFUND = "refund"

@dataclass
class PaymentItem:
    id: str
    price: int
    quantity: int
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    merchant_name: Optional[str] = None

    def to_midtrans_format(self) -> Dict:
        return {
            "id": self.id,
            "price": self.price,
            "quantity": self.quantity,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "merchant_name": self.merchant_name
        }

@dataclass
class CustomerInfo:
    first_name: str
    last_name: str
    email: str
    phone: str
    billing_address: Optional[Dict] = None
    shipping_address: Optional[Dict] = None

    def to_midtrans_format(self) -> Dict:
        customer_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone
        }
        
        if self.billing_address:
            customer_data["billing_address"] = self.billing_address
            
        if self.shipping_address:
            customer_data["shipping_address"] = self.shipping_address
            
        return customer_data

@dataclass
class PaymentTransaction:
    transaction_id: str
    order_id: str
    gross_amount: int
    payment_type: str
    transaction_status: str
    transaction_time: datetime
    settlement_time: Optional[datetime] = None
    payment_method: Optional[str] = None
    va_number: Optional[str] = None
    payment_url: Optional[str] = None
    qr_code: Optional[str] = None
    deeplink_redirect_url: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        data = asdict(self)
        # Convert datetime objects to ISO string
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @staticmethod
    def from_midtrans_response(response: Dict) -> 'PaymentTransaction':
        """Convert Midtrans response to PaymentTransaction object."""
        return PaymentTransaction(
            transaction_id=response.get('transaction_id'),
            order_id=response.get('order_id'),
            gross_amount=int(response.get('gross_amount', 0)),
            payment_type=response.get('payment_type'),
            transaction_status=response.get('transaction_status'),
            transaction_time=datetime.fromisoformat(response.get('transaction_time').replace('Z', '+00:00')),
            settlement_time=datetime.fromisoformat(response.get('settlement_time').replace('Z', '+00:00')) if response.get('settlement_time') else None,
            payment_method=response.get('payment_type'),
            va_number=response.get('va_numbers', [{}])[0].get('va_number') if response.get('va_numbers') else None,
            payment_url=response.get('redirect_url'),
            qr_code=response.get('qr_string'),
            deeplink_redirect_url=response.get('deeplink_redirect_url'),
            expires_at=datetime.fromisoformat(response.get('expiry_time').replace('Z', '+00:00')) if response.get('expiry_time') else None
        )

def generate_order_id(prefix: str = "ORDER") -> str:
    """Generate unique order ID for Midtrans."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = str(uuid.uuid4())[:8].upper()
    return f"{prefix}-{timestamp}-{random_suffix}"

def create_snap_payment(order_id: str, gross_amount: int, items: List[PaymentItem], 
                       customer: CustomerInfo, 
                       payment_methods: List[str] = None,
                       custom_expiry: Optional[Dict] = None) -> Dict:
    """
    Buat payment menggunakan Midtrans Snap.
    
    Args:
        order_id: Unique order ID
        gross_amount: Total amount in IDR
        items: List of payment items
        customer: Customer information
        payment_methods: Allowed payment methods
        custom_expiry: Custom expiry time
    
    Returns:
        Dict: Snap token dan payment URL
    """
    try:
        if not snap:
            # Mock mode
            logger.warning("Midtrans not configured, using mock payment")
            return {
                "token": f"mock_snap_token_{order_id}",
                "redirect_url": f"https://app.sandbox.midtrans.com/snap/v1/transactions/mock_snap_token_{order_id}/pdf"
            }

        # Build transaction details
        transaction_details = {
            "order_id": order_id,
            "gross_amount": gross_amount
        }

        # Build item details
        item_details = [item.to_midtrans_format() for item in items]

        # Build customer details
        customer_details = customer.to_midtrans_format()

        # Build credit card settings (optional)
        credit_card_config = {
            "secure": True,
            "bank": "bca",  # Acquiring bank
            "installment": {
                "required": False,
                "terms": {
                    "bca": [3, 6, 12],
                    "bni": [3, 6, 12],
                    "mandiri": [3, 6, 12],
                    "cimb": [3, 6, 12]
                }
            }
        }

        # Build enabled payments (jika tidak spesifik, Midtrans akan enable semua)
        enabled_payments = payment_methods if payment_methods else [
            "credit_card", "gopay", "shopeepay", "other_qris", 
            "bca_va", "bni_va", "bri_va", "echannel", "other_va"
        ]

        # Build complete parameter
        param = {
            "transaction_details": transaction_details,
            "credit_card": credit_card_config,
            "item_details": item_details,
            "customer_details": customer_details,
            "enabled_payments": enabled_payments
        }

        # Add custom expiry if provided
        if custom_expiry:
            param["custom_expiry"] = custom_expiry

        # Create transaction
        transaction = snap.create_transaction(param)
        
        logger.info(f"Snap payment created for order {order_id}: {transaction.get('token')}")
        return {
            "token": transaction.get('token'),
            "redirect_url": transaction.get('redirect_url')
        }

    except Exception as e:
        logger.error(f"Error creating Snap payment for order {order_id}: {e}", exc_info=True)
        raise

def create_direct_payment(order_id: str, gross_amount: int, items: List[PaymentItem],
                         customer: CustomerInfo, payment_method: str,
                         payment_details: Optional[Dict] = None) -> PaymentTransaction:
    """
    Buat direct payment (tidak menggunakan Snap) untuk method tertentu.
    
    Args:
        order_id: Unique order ID
        gross_amount: Total amount in IDR
        items: List of payment items  
        customer: Customer information
        payment_method: Specific payment method (gopay, bca_va, etc.)
        payment_details: Additional payment details (optional)
    
    Returns:
        PaymentTransaction: Transaction details
    """
    try:
        if not core_api:
            # Mock mode
            logger.warning("Midtrans not configured, using mock direct payment")
            return PaymentTransaction(
                transaction_id=f"mock_txn_{order_id}",
                order_id=order_id,
                gross_amount=gross_amount,
                payment_type=payment_method,
                transaction_status="pending",
                transaction_time=datetime.utcnow(),
                payment_url=f"https://mock-payment.example.com/{payment_method}/{order_id}"
            )

        # Build transaction details
        transaction_details = {
            "order_id": order_id,
            "gross_amount": gross_amount
        }

        # Build item details
        item_details = [item.to_midtrans_format() for item in items]

        # Build customer details
        customer_details = customer.to_midtrans_format()

        # Build payment method specific details
        payment_config = {}
        
        if payment_method == "gopay":
            payment_config = {
                "payment_type": "gopay",
                "gopay": {
                    "enable_callback": True,
                    "callback_url": "https://your-app.com/payment-callback"
                }
            }
        elif payment_method.endswith("_va"):  # Virtual Account
            bank = payment_method.replace("_va", "").upper()
            payment_config = {
                "payment_type": "bank_transfer",
                "bank_transfer": {
                    "bank": bank.lower()
                }
            }
        elif payment_method == "shopeepay":
            payment_config = {
                "payment_type": "shopeepay",
                "shopeepay": {
                    "callback_url": "https://your-app.com/payment-callback"
                }
            }
        
        # Update dengan payment_details jika ada
        if payment_details:
            payment_config.update(payment_details)

        # Build complete parameter
        param = {
            "transaction_details": transaction_details,
            "item_details": item_details,
            "customer_details": customer_details,
            **payment_config
        }

        # Create transaction
        transaction = core_api.charge(param)
        
        # Convert to PaymentTransaction object
        payment_txn = PaymentTransaction.from_midtrans_response(transaction)
        
        logger.info(f"Direct payment created for order {order_id} via {payment_method}")
        return payment_txn

    except Exception as e:
        logger.error(f"Error creating direct payment for order {order_id}: {e}", exc_info=True)
        raise

def check_transaction_status(order_id: str) -> Optional[PaymentTransaction]:
    """
    Check transaction status dari Midtrans.
    
    Args:
        order_id: Order ID untuk dicek
    
    Returns:
        PaymentTransaction: Status transaksi terkini
    """
    try:
        if not core_api:
            # Mock mode
            logger.warning("Midtrans not configured, returning mock status")
            return PaymentTransaction(
                transaction_id=f"mock_txn_{order_id}",
                order_id=order_id,
                gross_amount=100000,
                payment_type="mock",
                transaction_status="settlement",
                transaction_time=datetime.utcnow()
            )

        # Get transaction status
        status_response = core_api.transactions.status(order_id)
        
        # Convert to PaymentTransaction object
        payment_txn = PaymentTransaction.from_midtrans_response(status_response)
        
        logger.info(f"Transaction status checked for order {order_id}: {payment_txn.transaction_status}")
        return payment_txn

    except Exception as e:
        logger.error(f"Error checking transaction status for order {order_id}: {e}", exc_info=True)
        return None

def verify_webhook_signature(payload: str, signature: str) -> bool:
    """
    Verify webhook signature dari Midtrans untuk security.
    
    Args:
        payload: Raw payload dari webhook
        signature: Signature header dari Midtrans
    
    Returns:
        bool: True jika signature valid
    """
    try:
        if not MIDTRANS_SERVER_KEY or MIDTRANS_SERVER_KEY == "mock_server_key":
            # Mock mode - always return True
            return True
            
        # Generate signature
        expected_signature = hmac.new(
            MIDTRANS_SERVER_KEY.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, signature)
        
    except Exception as e:
        logger.error(f"Error verifying webhook signature: {e}", exc_info=True)
        return False

def process_webhook_notification(payload: Dict) -> bool:
    """
    Process webhook notification dari Midtrans.
    
    Args:
        payload: Webhook payload dari Midtrans
    
    Returns:
        bool: True jika berhasil diproses
    """
    try:
        order_id = payload.get('order_id')
        transaction_status = payload.get('transaction_status')
        fraud_status = payload.get('fraud_status')
        
        if not order_id:
            logger.error("Order ID not found in webhook payload")
            return False

        # Import di dalam function untuk avoid circular import
        from .orders_service import update_order_status, OrderStatus, get_order_by_id

        logger.info(f"Processing webhook for order {order_id}: status={transaction_status}, fraud={fraud_status}")

        # Update transaction record di database
        transaction_ref = db.collection('payment_transactions').document(order_id)
        transaction_ref.set({
            'order_id': order_id,
            'transaction_status': transaction_status,
            'fraud_status': fraud_status,
            'webhook_received_at': datetime.utcnow(),
            'full_payload': payload
        }, merge=True)

        # Process berdasarkan status
        if transaction_status == 'settlement':
            if fraud_status in ['accept', None]:
                # Payment success
                logger.info(f"Payment successful for order {order_id}")
                update_order_status(order_id, OrderStatus.PROCESSING)
                
                # Trigger next steps (assign driver, etc.)
                try:
                    order = get_order_by_id(order_id)
                    if order and order.delivery_address:
                        from .drivers_service import find_and_assign_nearest_driver
                        assigned_driver = find_and_assign_nearest_driver(
                            order_id, 
                            order.delivery_address
                        )
                        if assigned_driver:
                            logger.info(f"Driver {assigned_driver} assigned to order {order_id}")
                        else:
                            logger.warning(f"No available driver found for order {order_id}")
                except Exception as e:
                    logger.error(f"Error assigning driver for order {order_id}: {e}")
                    
            elif fraud_status == 'challenge':
                # Manual review required
                logger.warning(f"Payment requires manual review for order {order_id}")
                update_order_status(order_id, OrderStatus.PENDING_REVIEW)
            else:
                # Fraud detected
                logger.warning(f"Fraudulent payment detected for order {order_id}")
                update_order_status(order_id, OrderStatus.FAILED)
                
        elif transaction_status in ['pending']:
            # Payment pending
            logger.info(f"Payment pending for order {order_id}")
            update_order_status(order_id, OrderStatus.PENDING_PAYMENT)
            
        elif transaction_status in ['cancel', 'deny', 'expire', 'failure']:
            # Payment failed/cancelled
            logger.warning(f"Payment failed/cancelled for order {order_id}: {transaction_status}")
            update_order_status(order_id, OrderStatus.FAILED)
            
        return True

    except Exception as e:
        logger.error(f"Error processing webhook notification: {e}", exc_info=True)
        return False

def cancel_transaction(order_id: str) -> bool:
    """
    Cancel/expire transaction.
    
    Args:
        order_id: Order ID untuk dicancel
    
    Returns:
        bool: True jika berhasil dicancel
    """
    try:
        if not core_api:
            logger.warning("Midtrans not configured, mock cancel")
            return True
            
        # Cancel transaction
        cancel_response = core_api.transactions.cancel(order_id)
        
        logger.info(f"Transaction cancelled for order {order_id}")
        return cancel_response.get('status_code') == '200'

    except Exception as e:
        logger.error(f"Error cancelling transaction for order {order_id}: {e}", exc_info=True)
        return False

def initiate_refund(order_id: str, refund_amount: Optional[int] = None, reason: str = "Customer request") -> bool:
    """
    Initiate refund untuk transaction yang sudah settlement.
    
    Args:
        order_id: Order ID untuk refund
        refund_amount: Amount to refund (partial), None for full refund
        reason: Reason for refund
    
    Returns:
        bool: True jika refund berhasil diinisiasi
    """
    try:
        if not core_api:
            logger.warning("Midtrans not configured, mock refund")
            return True

        # Build refund parameter
        refund_params = {
            "refund_key": f"refund-{order_id}-{int(datetime.utcnow().timestamp())}",
            "reason": reason
        }
        
        if refund_amount:
            refund_params["amount"] = refund_amount

        # Initiate refund
        refund_response = core_api.transactions.refund(order_id, refund_params)
        
        # Save refund record
        refund_ref = db.collection('payment_refunds').document()
        refund_ref.set({
            'order_id': order_id,
            'refund_amount': refund_amount,
            'reason': reason,
            'refund_key': refund_params["refund_key"],
            'status': refund_response.get('status_message'),
            'created_at': datetime.utcnow(),
            'midtrans_response': refund_response
        })
        
        logger.info(f"Refund initiated for order {order_id}: amount={refund_amount}")
        return refund_response.get('status_code') in ['200', '201']

    except Exception as e:
        logger.error(f"Error initiating refund for order {order_id}: {e}", exc_info=True)
        return False