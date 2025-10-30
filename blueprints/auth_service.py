from firebase_admin import auth, firestore
from firebase_config import get_auth_client, get_firestore_client
from logger_config import get_logger
import time
import re

# Inisialisasi Logger untuk modul ini
logger = get_logger('AuthService')

# Inisialisasi Klien Firebase
firebase_auth = get_auth_client()
db = get_firestore_client()

# Nama koleksi Firestore untuk data profil tambahan
USER_PROFILE_COLLECTION = 'user_profiles'

def _is_valid_phone(phone_number: str) -> bool:
    """Memvalidasi format nomor telepon (minimal 10 digit, hanya angka)."""
    # Menghapus spasi dan tanda hubung
    cleaned_number = re.sub(r'\D', '', phone_number)
    return len(cleaned_number) >= 10 and cleaned_number.startswith('62')

def check_onboarding_status(uid: str) -> dict:
    """
    Memeriksa status onboarding (A. Introduce) pengguna. 
    Digunakan saat aplikasi dimuat (A. Loading_start/middle).
    
    Args:
        uid (str): ID pengguna dari Firebase Auth.
        
    Returns:
        dict: Status pengguna dan langkah terakhir yang harus dilalui.
    """
    logger.info(f"Memeriksa status onboarding untuk UID: {uid}")
    try:
        user_ref = db.collection(USER_PROFILE_COLLECTION).document(uid)
        doc = user_ref.get()
        
        if not doc.exists:
            # Pengguna terdaftar di Auth tetapi belum mengisi profil (E)
            return {"status": "NEW_USER", "next_step": "SET_PROFILE"}
        
        profile_data = doc.to_dict()
        
        # Mengecek kelengkapan profil
        if not all(profile_data.get(field) for field in ['full_name', 'email', 'birth_date']):
             return {"status": "INCOMPLETE_PROFILE", "next_step": "SET_PROFILE"}
             
        # Mengecek setting keamanan (F/G)
        if not profile_data.get('pin_set') and not profile_data.get('touch_id_set'):
            return {"status": "PROFILE_COMPLETE", "next_step": "SET_SECURITY"}
        
        # Semua selesai, menuju Home (H)
        return {"status": "ALL_COMPLETE", "next_step": "HOME"}
        
    except Exception as e:
        logger.error(f"Gagal memeriksa status onboarding UID {uid}: {e}", exc_info=True)
        return {"status": "ERROR", "next_step": "ERROR_PAGE"}


# --- Fungsi Otentikasi Dasar (B & C) ---

def register_user(phone_number: str, password: str, device_id: str) -> dict:
    """
    Mendaftarkan pengguna baru (C. Signup).
    Catatan: Firebase Auth biasanya menangani verifikasi OTP (D) 
    sebelum user ini dibuat. Kita asumsikan ini adalah langkah setelah verifikasi sukses.

    Args:
        phone_number (str): Nomor telepon pengguna.
        password (str): Kata sandi pengguna.
        device_id (str): ID perangkat untuk keamanan.

    Returns:
        dict: Hasil registrasi dan Custom Token jika berhasil.
    """
    if not _is_valid_phone(phone_number):
        return {"success": False, "message": "Format nomor telepon tidak valid."}
        
    logger.info(f"Mencoba registrasi untuk: {phone_number}")
    
    try:
        # 1. Buat user di Firebase Authentication
        user = firebase_auth.create_user(
            phone_number=f'+{phone_number}', # Format internasional wajib
            password=password,
            display_name=None,
            disabled=False
        )
        
        uid = user.uid
        
        # 2. Buat dokumen profil awal di Firestore
        profile_data = {
            "created_at": firestore.SERVER_TIMESTAMP,
            "last_login": firestore.SERVER_TIMESTAMP,
            "phone_number": phone_number,
            "full_name": None, # Akan diisi di langkah E
            "email": None,
            "pin_set": False, # Untuk langkah G
            "touch_id_set": False, # Untuk langkah F
            "role": "customer",
            "device_ids": [device_id]
        }
        db.collection(USER_PROFILE_COLLECTION).document(uid).set(profile_data)
        
        # 3. Buat Custom Token untuk login otomatis (opsional)
        custom_token = firebase_auth.create_custom_token(uid)
        
        logger.info(f"Pengguna baru berhasil dibuat dengan UID: {uid}")
        
        return {
            "success": True, 
            "uid": uid, 
            "custom_token": custom_token.decode('utf-8'),
            "message": "Registrasi berhasil. Lanjutkan ke atur profil."
        }
    except auth.PhoneNumberAlreadyExistsError:
        logger.warning(f"Registrasi gagal: Nomor {phone_number} sudah terdaftar.")
        return {"success": False, "message": "Nomor telepon ini sudah terdaftar."}
    except Exception as e:
        logger.error(f"Registrasi gagal karena kesalahan server: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat registrasi."}

def login_user(uid: str, device_id: str) -> dict:
    """
    Login pengguna (B. Login) dan membuat Custom Token.
    Asumsi: Login/Password sudah diverifikasi oleh Firebase Auth di sisi klien, 
    atau fungsi ini dipanggil setelah OTP sukses.

    Args:
        uid (str): ID pengguna.
        device_id (str): ID perangkat untuk validasi.
        
    Returns:
        dict: Custom Token dan status profil.
    """
    logger.info(f"Mencoba login untuk UID: {uid}")
    try:
        # 1. Update timestamp login dan device ID
        user_ref = db.collection(USER_PROFILE_COLLECTION).document(uid)
        user_ref.update({
            "last_login": firestore.SERVER_TIMESTAMP,
            "device_ids": firestore.ArrayUnion([device_id])
        })
        
        # 2. Buat Custom Token untuk sesi
        custom_token = firebase_auth.create_custom_token(uid)
        
        # 3. Cek status onboarding untuk menentukan navigasi selanjutnya
        onboarding_status = check_onboarding_status(uid)
        
        logger.info(f"Login berhasil. Status: {onboarding_status['next_step']}")

        return {
            "success": True,
            "custom_token": custom_token.decode('utf-8'),
            "next_step": onboarding_status['next_step'],
            "message": "Login berhasil."
        }
        
    except Exception as e:
        logger.error(f"Login gagal untuk UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat login."}


# --- Fungsi Update Profil & Keamanan (E, F, G) ---

def update_user_profile(uid: str, name: str, email: str, birth_date: str) -> dict:
    """
    Memperbarui profil pengguna (E. Set Your Profile).
    
    Args:
        uid (str): ID pengguna.
        name (str): Nama lengkap (E. your profile_Filled).
        email (str): Email (E. your profile_Filled).
        birth_date (str): Tanggal lahir.

    Returns:
        dict: Status pembaruan.
    """
    logger.info(f"Memperbarui profil untuk UID: {uid}")
    try:
        user_ref = db.collection(USER_PROFILE_COLLECTION).document(uid)
        update_data = {
            "full_name": name,
            "email": email,
            "birth_date": birth_date,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        user_ref.update(update_data)
        
        # Opsi: Update display name di Firebase Auth juga
        firebase_auth.update_user(uid, display_name=name)
        
        return {"success": True, "message": "Profil berhasil diperbarui."}
    except Exception as e:
        logger.error(f"Gagal memperbarui profil UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Gagal memperbarui profil."}

def set_user_security_setting(uid: str, security_type: str, is_set: bool) -> dict:
    """
    Mengatur status keamanan (F. Set Touch Id atau G. Set PIN Security).
    
    Args:
        uid (str): ID pengguna.
        security_type (str): 'pin' atau 'touch_id'.
        is_set (bool): Status True/False.
    """
    if security_type not in ['pin', 'touch_id']:
        return {"success": False, "message": "Tipe keamanan tidak valid."}
        
    try:
        key = f"{security_type}_set"
        db.collection(USER_PROFILE_COLLECTION).document(uid).update({
            key: is_set,
            "updated_at": firestore.SERVER_TIMESTAMP,
        })
        logger.info(f"Keamanan {security_type} untuk UID {uid} diatur ke {is_set}.")
        return {"success": True, "message": f"Pengaturan {security_type} berhasil diperbarui."}
    except Exception as e:
        logger.error(f"Gagal mengatur keamanan {security_type} untuk UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Gagal menyimpan pengaturan keamanan."}


# --- Fungsi Manajemen Akun (Y) ---

def get_user_profile(uid: str) -> dict:
    """
    Mengambil detail profil pengguna (Y. Profile).
    
    Args:
        uid (str): ID pengguna.

    Returns:
        dict: Data profil atau error.
    """
    try:
        doc = db.collection(USER_PROFILE_COLLECTION).document(uid).get()
        if doc.exists:
            return {"success": True, "data": doc.to_dict()}
        else:
            return {"success": False, "message": "Data profil tidak ditemukan."}
    except Exception as e:
        logger.error(f"Gagal mengambil profil UID {uid}: {e}", exc_info=True)
        return {"success": False, "message": "Kesalahan server saat mengambil profil."}


# --- Catatan untuk Fungsi OTP (D) ---
# D. Otp code verification: Dalam praktik sebenarnya, mengirim dan memverifikasi OTP 
# biasanya dilakukan di SISI KLIEN menggunakan Firebase Authentication SDK 
# (signInWithPhoneNumber) karena alasan keamanan (reCAPTCHA, limitasi rate).
# Backend Python hanya akan berurusan dengan pengguna setelah terverifikasi (UID sudah didapat).
