# seed_data.py

import os
import json
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()

def seed_data():
    """Mengisi database dengan data awal dari file JSON."""
    seed_files = ["foods.json", "drivers.json", "promotions.json"]

    for seed_file in seed_files:
        collection_name = seed_file.split('.')[0]
        try:
            with open(f"./seed_data/{seed_file}", "r") as f:
                data = json.load(f)

            for item in data:
                doc_id = item.get('id') # Gunakan ID dari JSON jika ada
                doc_ref = db.collection(collection_name).document(doc_id)
                doc_ref.set(item)
                logger.info(f"Data '{doc_id}' berhasil ditambahkan ke koleksi '{collection_name}'.")

        except Exception as e:
            logger.error(f"Gagal memuat data dari {seed_file}: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Memulai proses seeding data...")
    seed_data()
    logger.info("Proses seeding data selesai.")
