# blueprints/data_catalog_service.py

from dataclasses import dataclass, asdict
from typing import List, Optional
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()

FOOD_COLLECTION = 'foods'
PROMOTION_COLLECTION = 'promotions'

# --- Model Data ---
# Menggunakan dataclass untuk validasi tipe data dasar dan struktur yang jelas.

@dataclass
class FoodItem:
    id: str
    name: str
    price: float
    description: str
    image_url: str
    category: str

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'FoodItem':
        """Membuat instance FoodItem dari kamus Firestore."""
        return FoodItem(
            id=doc_id,
            name=data.get('name'),
            price=float(data.get('price', 0.0)),
            description=data.get('description'),
            image_url=data.get('image_url'),
            category=data.get('category')
        )

    def to_dict(self) -> dict:
        """Mengonversi instance FoodItem menjadi kamus."""
        return asdict(self)

@dataclass
class Promotion:
    id: str
    title: str
    description: str
    promo_code: Optional[str]
    image_url: str

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'Promotion':
        """Membuat instance Promotion dari kamus Firestore."""
        return Promotion(
            id=doc_id,
            title=data.get('title'),
            description=data.get('description'),
            promo_code=data.get('promo_code'),
            image_url=data.get('image_url')
        )

    def to_dict(self) -> dict:
        """Mengonversi instance Promotion menjadi kamus."""
        return asdict(self)


# --- Fungsi Layanan ---

def get_all_food_items() -> List[FoodItem]:
    """
    Mengambil semua item makanan dari koleksi 'foods'.
    Memunculkan Exception jika terjadi kesalahan.
    """
    try:
        food_ref = db.collection(FOOD_COLLECTION)
        food_list = [FoodItem.from_dict(doc.id, doc.to_dict()) for doc in food_ref.stream()]
        logger.info(f"Berhasil mengambil {len(food_list)} item makanan.")
        return food_list
    except Exception as e:
        logger.error(f"Gagal mengambil item makanan: {e}", exc_info=True)
        raise RuntimeError("Gagal berkomunikasi dengan database untuk mengambil data makanan.") from e

def get_all_promotions() -> List[Promotion]:
    """
    Mengambil semua promosi dari koleksi 'promotions'.
    Memunculkan Exception jika terjadi kesalahan.
    """
    try:
        promo_ref = db.collection(PROMOTION_COLLECTION)
        promo_list = [Promotion.from_dict(doc.id, doc.to_dict()) for doc in promo_ref.stream()]
        logger.info(f"Berhasil mengambil {len(promo_list)} promosi.")
        return promo_list
    except Exception as e:
        logger.error(f"Gagal mengambil promosi: {e}", exc_info=True)
        raise RuntimeError("Gagal berkomunikasi dengan database untuk mengambil data promosi.") from e
