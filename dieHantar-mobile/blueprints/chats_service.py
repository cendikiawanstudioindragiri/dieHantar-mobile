# blueprints/chats_service.py

from dataclasses import dataclass, asdict, field
from typing import List, Optional
import datetime
from firebase_admin import firestore
from firebase_config import get_firestore_client
from logger_config import get_logger
# Pertahankan impor ini karena chat sangat terkait dengan pesanan dan notifikasi
from . import notification_service
from .orders_service import ORDERS_COLLECTION, Order # Gunakan layanan order yang sudah dimodernisasi

logger = get_logger(__name__)
db = get_firestore_client()
MESSAGES_SUBCOLLECTION = 'messages'

@dataclass
class ChatMessage:
    id: str
    order_id: str
    sender_id: str
    receiver_id: str
    text: str
    timestamp: datetime.datetime

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(doc_id: str, order_id: str, data: dict) -> 'ChatMessage':
        return ChatMessage(
            id=doc_id,
            order_id=order_id,
            sender_id=data.get('sender_id'),
            receiver_id=data.get('receiver_id'),
            text=data.get('text'),
            timestamp=data.get('timestamp')
        )

def send_message(order_id: str, sender_id: str, text: str) -> ChatMessage:
    if not all([order_id, sender_id, text]):
        raise ValueError("ID Pesanan, ID pengirim, dan teks pesan diperlukan.")

    try:
        order_ref = db.collection(ORDERS_COLLECTION).document(order_id)
        order_doc = order_ref.get()
        if not order_doc.exists:
            raise ValueError(f"Pesanan dengan ID {order_id} tidak ditemukan.")

        order_data = order_doc.to_dict()
        user_id = order_data.get('user_id')
        driver_id = order_data.get('driver_id')

        if sender_id not in [user_id, driver_id]:
            logger.warning(f"Akses ditolak: Pengguna {sender_id} mencoba mengirim pesan ke pesanan {order_id}.")
            raise PermissionError("Anda tidak diizinkan mengirim pesan ke pesanan ini.")
        
        receiver_id = driver_id if sender_id == user_id else user_id
        if not receiver_id:
            raise ValueError("Penerima pesan tidak ditemukan (kemungkinan driver belum ditugaskan).")

        message_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'text': text,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        
        # Simpan pesan dan dapatkan referensinya
        update_time, message_ref = order_ref.collection(MESSAGES_SUBCOLLECTION).add(message_data)
        
        # Kirim notifikasi sebagai efek samping (side effect)
        notification_service.send_fcm_notification(
            uid=receiver_id,
            title=f"Pesan Baru untuk Pesanan Anda",
            body=text,
            data={'order_id': order_id, 'type': 'NEW_CHAT_MESSAGE'}
        )

        # Ambil data yang baru disimpan untuk dikembalikan
        new_message_doc = message_ref.get()
        return ChatMessage.from_dict(new_message_doc.id, order_id, new_message_doc.to_dict())

    except (ValueError, PermissionError):
        raise
    except Exception as e:
        logger.error(f"Gagal mengirim pesan untuk pesanan {order_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal menyimpan pesan atau mengirim notifikasi.") from e

def get_chat_history(order_id: str, requester_id: str) -> List[ChatMessage]:
    try:
        order_ref = db.collection(ORDERS_COLLECTION).document(order_id)
        order_doc = order_ref.get()
        if not order_doc.exists:
            raise ValueError(f"Pesanan dengan ID {order_id} tidak ditemukan.")

        order_data = order_doc.to_dict()
        if requester_id not in [order_data.get('user_id'), order_data.get('driver_id')]:
            logger.warning(f"Akses ditolak: Pengguna {requester_id} mencoba melihat chat pesanan {order_id}.")
            raise PermissionError("Anda tidak diizinkan melihat riwayat obrolan ini.")

        messages_ref = order_ref.collection(MESSAGES_SUBCOLLECTION).order_by('timestamp', direction=firestore.Query.ASCENDING)
        message_docs = messages_ref.stream()
        
        chat_history = [ChatMessage.from_dict(doc.id, order_id, doc.to_dict()) for doc in message_docs]
        return chat_history

    except (ValueError, PermissionError):
        raise
    except Exception as e:
        logger.error(f"Gagal mengambil riwayat chat untuk pesanan {order_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal mengambil riwayat obrolan dari database.") from e
