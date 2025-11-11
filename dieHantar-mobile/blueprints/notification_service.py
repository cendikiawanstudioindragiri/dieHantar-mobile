# blueprints/notification_service.py

from firebase_admin import messaging
from logger_config import get_logger
from firebase_config import get_firestore_client

# Inisialisasi Logger
logger = get_logger('NotificationService')
db = get_firestore_client()

def get_user_fcm_token(uid: str) -> str:
    """
    Mengambil token registrasi FCM dari database Firestore.
    Diasumsikan token disimpan dalam koleksi 'users' pada dokumen pengguna.
    """
    try:
        user_doc = db.collection('users').document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict().get('fcm_token')
        return None
    except Exception as e:
        logger.error(f"Gagal mengambil FCM token untuk UID {uid}: {e}")
        return None

def send_fcm_notification(uid: str, title: str, body: str, data: dict = None) -> bool:
    """
    Mengirim notifikasi push ke perangkat pengguna melalui FCM.

    Args:
        uid (str): ID pengguna yang akan dikirimi notifikasi.
        title (str): Judul notifikasi.
        body (str): Isi pesan notifikasi.
        data (dict, optional): Data tambahan yang akan dikirim bersama notifikasi.

    Returns:
        bool: True jika notifikasi berhasil dikirim, False jika gagal.
    """
    fcm_token = get_user_fcm_token(uid)

    if not fcm_token:
        logger.warning(f"Tidak dapat mengirim notifikasi: FCM token untuk UID {uid} tidak ditemukan.")
        return False

    # Buat payload notifikasi
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=fcm_token,
    )

    try:
        # Kirim pesan menggunakan Firebase Admin SDK
        response = messaging.send(message)
        logger.info(f"Notifikasi berhasil dikirim ke UID {uid}: {response}")
        return True
    except Exception as e:
        logger.error(f"Gagal mengirim notifikasi FCM ke UID {uid}: {e}", exc_info=True)
        return False
