import firebase_admin
from firebase_admin import credentials, firestore, auth, messaging

def initialize_firebase_admin():
    """
    Menginisialisasi Firebase Admin SDK jika belum ada. 
    Fungsi ini sekarang aman untuk dipanggil berkali-kali (idempotent).
    """
    # Cek apakah aplikasi default sudah ada sebelum mencoba inisialisasi
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate("firebase-service-account.json")
            firebase_admin.initialize_app(cred)
            print("INFO: Firebase Admin SDK berhasil diinisialisasi.")
        except FileNotFoundError:
            print("WARNING: File 'firebase-service-account.json' tidak ditemukan. Mencoba inisialisasi default (untuk lingkungan Google Cloud).")
            try:
                firebase_admin.initialize_app()
                print("INFO: Berhasil inisialisasi Firebase Admin secara default.")
            except ValueError:
                print("FATAL: Gagal total menginisialisasi Firebase Admin. Kredensial tidak ditemukan.")
                # Hentikan aplikasi jika tidak ada kredensial sama sekali
                raise
    # Jika sudah ada, tidak perlu melakukan apa-apa.

def get_firestore_client():
    """Mengembalikan instance Firestore client. Menginisialisasi app jika perlu."""
    initialize_firebase_admin() # Memastikan SDK siap digunakan
    return firestore.client()

def get_auth_client():
    """Mengembalikan instance Auth client. Menginisialisasi app jika perlu."""
    initialize_firebase_admin() # Memastikan SDK siap digunakan
    return auth

def send_fcm_notification(token, title, body, data=None):
    """
    Mengirim notifikasi push ke perangkat menggunakan Firebase Cloud Messaging (FCM).
    """
    initialize_firebase_admin() # Memastikan SDK siap digunakan
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=token,
        )
        
        response = messaging.send(message)
        print(f"INFO: Notifikasi berhasil dikirim: {response}")
        return response
    except Exception as e:
        print(f"ERROR: Gagal mengirim notifikasi: {e}")
        return None
