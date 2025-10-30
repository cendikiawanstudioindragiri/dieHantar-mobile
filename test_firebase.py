
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

print("Memulai pengujian inisialisasi Firebase...")
print("="*40)

# Simpan aplikasi yang berhasil diinisialisasi
successful_app = None

# --- Metode 1: Application Default Credentials (ADC) ---
try:
    print("\n[Metode 1] Mencoba inisialisasi dengan Application Default Credentials (ADC)...")
    # Pastikan GOOGLE_APPLICATION_CREDENTIALS di-set di shell
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        print(f"Variabel lingkungan GOOGLE_APPLICATION_CREDENTIALS ditemukan: {os.environ['GOOGLE_APPLICATION_CREDENTIALS']}")
        
        # Hapus instance aplikasi default jika ada
        if firebase_admin._apps:
            for app in list(firebase_admin._apps.values()):
                firebase_admin.delete_app(app)

        # Inisialisasi menggunakan ADC
        cred_adc = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred_adc, name='adc_app')
        db = firestore.client(app=firebase_admin.get_app('adc_app'))
        print("✅ Inisialisasi ADC BERHASIL.")
        successful_app = 'adc_app'
    else:
        print("⚠️ Variabel lingkungan GOOGLE_APPLICATION_CREDENTIALS tidak di-set.")

except Exception as e:
    print(f"❌ Inisialisasi ADC GAGAL: {e}")

print("="*40)

# --- Metode 2: Memuat file JSON secara manual ---
try:
    print("\n[Metode 2] Mencoba inisialisasi dengan memuat file JSON secara manual...")
    
    key_path = "dieHantar-app/serviceAccountKey.json"
    print(f"Membaca file kunci dari: {key_path}")

    with open(key_path, 'r', encoding='utf-8') as f:
        service_account_info = json.load(f)

    # Memperbaiki private_key secara manual di memori
    # Ini adalah penyebab paling umum dari masalah PEM di JSON
    service_account_info['private_key'] = service_account_info['private_key'].replace('\\n', '\n')

    cred_manual = credentials.Certificate(service_account_info)
    
    # Hapus instance aplikasi default jika ada
    if firebase_admin._apps:
        for app in list(firebase_admin._apps.values()):
            if app.name == firebase_admin.DEFAULT_APP_NAME or app.name == 'manual_app':
                 firebase_admin.delete_app(app)

    firebase_admin.initialize_app(cred_manual, name='manual_app')
    db = firestore.client(app=firebase_admin.get_app('manual_app'))
    print("✅ Inisialisasi manual BERHASIL.")
    if not successful_app:
        successful_app = 'manual_app'

except Exception as e:
    print(f"❌ Inisialisasi manual GAGAL: {e}")

print("="*40)

if successful_app:
    print(f"\n🎉 Pengujian Selesai. Setidaknya satu metode inisialisasi berhasil (aplikasi: '{successful_app}').")
else:
    print("\n😭 Pengujian Selesai. Semua metode inisialisasi gagal.")

# Cleanup semua aplikasi yang mungkin dibuat
for app in list(firebase_admin._apps.values()):
    firebase_admin.delete_app(app)
