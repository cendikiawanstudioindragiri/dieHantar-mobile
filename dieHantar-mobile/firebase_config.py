# firebase_config.py

import os
import json
import logging
import firebase_admin
from firebase_admin import credentials, firestore, auth, messaging

# Siapkan logger untuk modul ini
logger = logging.getLogger(__name__)

def initialize_firebase():
    """
    Menginisialisasi Firebase Admin SDK jika belum ada. Idempotent.
    
    Mencoba mengambil kredensial dari variabel lingkungan FIREBASE_CREDENTIALS_JSON.
    Jika tidak ada, akan kembali ke default (berguna untuk Google Cloud Environments seperti App Hosting).
    """
    if not firebase_admin._apps:
        try:
            firebase_credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON')
            
            if firebase_credentials_json:
                logger.info("Menginisialisasi Firebase dari FIREBASE_CREDENTIALS_JSON...")
                cred_dict = json.loads(firebase_credentials_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                logger.info("FIREBASE_CREDENTIALS_JSON tidak disetel. Menggunakan kredensial default aplikasi...")
                # Ini adalah metode yang disarankan untuk lingkungan Google Cloud (termasuk Firebase App Hosting)
                firebase_admin.initialize_app()
            
            logger.info("Firebase Admin SDK berhasil diinisialisasi.")

        except Exception as e:
            logger.critical(f"FATAL: Gagal menginisialisasi Firebase Admin SDK: {e}", exc_info=True)
            # Gagal pada tahap ini bersifat fatal, jadi kita sebarkan pengecualiannya
            # agar aplikasi gagal启动 daripada berjalan dalam keadaan rusak.
            raise

def get_firestore_client():
    """Mengembalikan instance Firestore client. Memastikan SDK sudah diinisialisasi."""
    if not firebase_admin._apps:
        initialize_firebase()
    return firestore.client()

def get_auth_client():
    """Mengembalikan instance Auth client. Memastikan SDK sudah diinisialisasi."""
    if not firebase_admin._apps:
        initialize_firebase()
    return auth

def get_messaging_client():
    """Mengembalikan instance Messaging client. Memastikan SDK sudah diinisialisasi."""
    if not firebase_admin._apps:
        initialize_firebase()
    return messaging
