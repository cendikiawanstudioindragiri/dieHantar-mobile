# Proyek dieHantar: Aplikasi Transportasi & Makanan

Selamat datang di proyek dieHantar, sebuah aplikasi berbasis Flask untuk layanan pesan-antar makanan dan transportasi.

## 🚀 Panduan Cepat

Untuk panduan interaktif lengkap, gunakan **CodeTour** extension di VS Code dan buka tour **"Panduan Orientasi Proyek dieHantar"** di folder `.tours/project_orientation.tour`.

Tour ini akan memandu Anda melalui:
1. 📁 Melihat struktur/daftar file di folder proyek
2. 💻 Membuka proyek di editor/IDE
3. 🌐 Menjalankan proyek agar bisa dilihat di browser
4. 🔍 Melihat info proyek (Git/GitHub/GCP)

## Struktur Proyek

Untuk melihat daftar lengkap file proyek, gunakan:
```bash
# Melihat struktur folder
ls -la

# Melihat tree struktur (jika tree terinstall)
tree

# Atau gunakan find untuk file Python
find . -type f -name "*.py" | grep -v __pycache__ | sort
```

Struktur folder utama:

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

## 💻 Membuka Proyek di Editor/IDE

### Project IDX (Google Cloud IDE)
Proyek ini dikonfigurasi untuk Project IDX dengan file `.idx/dev.nix`. Cukup buka di Project IDX dan environment akan disetup otomatis.

### VS Code Lokal
1. Clone repository:
   ```bash
   git clone https://github.com/cendikiawanstudios/dieHantar-mobile.git
   cd dieHantar-mobile
   ```

2. Buka di VS Code:
   ```bash
   code .
   ```

3. Install extensions yang direkomendasikan:
   - Python (Microsoft)
   - Thunder Client (untuk testing API)
   - CodeTour (untuk melihat panduan interaktif)

## 🌐 Cara Menjalankan

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

    Ada beberapa cara untuk menjalankan aplikasi:

    ```bash
    # Cara 1: Menggunakan development server
    python dev_server.py
    
    # Cara 2: Menggunakan script devserver.sh (di Project IDX)
    ./devserver.sh
    
    # Cara 3: Menggunakan Flask CLI
    flask run
    ```

5.  **Buka di Browser:**

    Setelah server berjalan, akses aplikasi di:
    ```
    http://localhost:8080/
    ```
    
    Health check endpoint akan mengembalikan:
    ```json
    {
      "status": "ok",
      "service": "dieHantar Super-App API"
    }
    ```

## 🔍 Informasi Proyek

### Git Repository
```bash
# Melihat remote repository
git remote -v

# Melihat branch
git branch -a

# Melihat history
git log --oneline -10
```

### GitHub Repository
- **Organization:** cendikiawanstudios
- **Repository:** dieHantar-mobile
- **URL:** https://github.com/cendikiawanstudios/dieHantar-mobile

```bash
# Menggunakan GitHub CLI
gh repo view cendikiawanstudios/dieHantar-mobile
gh repo view --web  # Buka di browser
```

### Google Cloud Platform (GCP)
Proyek ini menggunakan Firebase (bagian dari GCP):
- **Firebase Console:** https://console.firebase.google.com
- **GCP Console:** https://console.cloud.google.com

Environment variables yang dibutuhkan:
- `FIREBASE_CREDENTIALS_JSON` atau `GOOGLE_APPLICATION_CREDENTIALS`

## Pengujian

Untuk menjalankan tes, gunakan `pytest`:

```bash
pytest
```