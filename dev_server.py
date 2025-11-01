# dev_server.py

import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env. Penting untuk pengembangan lokal.
load_dotenv()

# Impor factory aplikasi dari main.py, yang sekarang menjadi sumber kebenaran tunggal.
from main import create_app

# Buat instance aplikasi menggunakan factory.
# Ini memastikan bahwa aplikasi pengembangan identik dengan aplikasi produksi.
app = create_app()

if __name__ == "__main__":
    # Jalankan server dalam mode debug pada port dari env atau default ke 8080
    app.run(
        debug=True, 
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 8080))
    )
