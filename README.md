# Proyek dieHantar: Aplikasi Transportasi & Makanan

Selamat datang di proyek dieHantar, sebuah aplikasi berbasis Flask untuk layanan pesan-antar makanan dan transportasi.

## Struktur Proyek

```
.dieHantar/
|-- blueprints/ # Modul-modul aplikasi (Blueprints)
|   |-- __init__.py
|   |-- auth/ # Otentikasi pengguna
|   |-- data_catalog/ # Data makanan & promosi
|   |-- driver/ # Logika terkait driver
|   |-- order/ # Manajemen pesanan
|   |-- data_catalog_service.py
|   |-- driver_service.py
|   `-- order_service.py
|-- seed_data/ # Data awal untuk database
|   |-- drivers.json
|   |-- foods.json
|   `-- promotions.json
|-- tests/ # Tes otomatis
|   `-- test_order_service.py
|-- .env # File untuk variabel lingkungan (JANGAN DI-COMMIT)
|-- .gitignore
|-- app.py # Titik masuk utama aplikasi Flask
|-- firebase_config.py # Konfigurasi Firebase
|-- logger_config.py # Konfigurasi logger
|-- README.md
|-- requirements.txt
`-- seed_data.py # Skrip untuk mengisi data awal
```

## Cara Menjalankan

1.  **Instal Dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Konfigurasi Firebase:**

    *   Buat proyek Firebase dan unduh file kunci layanan (service account key).
    *   Buat file `.env` di root proyek.
    *   Tambahkan variabel `FIREBASE_CREDENTIALS_JSON` ke file `.env` dan isikan dengan konten JSON kunci layanan Anda.

3.  **Isi Data Awal (Seed Data):**

    ```bash
    python seed_data.py
    ```

4.  **Jalankan Aplikasi:**

    ```bash
    flask run
    ```

## Pengujian

Untuk menjalankan tes, gunakan `pytest`:

```bash
pytest
```