#!/bin/sh

# Aktifkan virtual environment
source .venv/bin/activate

# Jalankan server pengembangan yang baru menggunakan python.
# Opsi -u memastikan bahwa output (seperti log) tidak di-buffer.
python -u dev_server.py
