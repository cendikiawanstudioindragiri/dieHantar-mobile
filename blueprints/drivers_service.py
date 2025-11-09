# blueprints/drivers_service.py

from dataclasses import dataclass, asdict
from typing import Optional, Dict
import datetime
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()
DRIVERS_COLLECTION = 'drivers'

class DriverStatus(Enum):
    OFFLINE = "offline"
    ONLINE = "online"      # Tersedia untuk menerima pesanan
    BUSY = "busy"          # Sedang dalam perjalanan atau menangani pesanan

@dataclass
class Driver:
    id: str
    name: str
    vehicle_type: str # e.g., 'MOTORCYCLE', 'CAR'
    status: str
    current_location: Optional[Dict] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'Driver':
        return Driver(
            id=doc_id,
            name=data.get('name'),
            vehicle_type=data.get('vehicle_type'),
            status=data.get('status'),
            current_location=data.get('current_location'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> dict:
        return asdict(self)

def get_driver_public_info(driver_id: str) -> Driver:
    if not driver_id:
        raise ValueError("ID Driver tidak boleh kosong.")
    try:
        doc_ref = db.collection(DRIVERS_COLLECTION).document(driver_id)
        doc = doc_ref.get()
        if not doc.exists:
            raise ValueError(f"Driver dengan ID {driver_id} tidak ditemukan.")
        return Driver.from_dict(doc.id, doc.to_dict())
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Gagal mengambil info driver {driver_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal mengambil data driver dari database.") from e

def update_driver_location(driver_id: str, lat: float, lon: float) -> None:
    if not all([driver_id, isinstance(lat, (int, float)), isinstance(lon, (int, float))]):
        raise ValueError("ID Driver, latitude, dan longitude diperlukan dan harus berupa angka.")
    
    location_data = {
        'current_location': {'lat': lat, 'lon': lon},
        'updated_at': datetime.datetime.utcnow()
    }
    try:
        doc_ref = db.collection(DRIVERS_COLLECTION).document(driver_id)
        # Gunakan merge=True untuk membuat dokumen jika belum ada, atau memperbarui jika sudah ada
        doc_ref.set(location_data, merge=True)
        logger.info(f"Lokasi driver {driver_id} diperbarui ke ({lat}, {lon})")
    except Exception as e:
        logger.error(f"Gagal memperbarui lokasi driver {driver_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal memperbarui lokasi driver di database.") from e

def find_and_assign_nearest_driver(order_id: str) -> Optional[str]:
    """Find and assign nearest available driver to an order (stub)."""
    # Stub implementation - returns None for now
    logger.info(f"Mencari driver untuk pesanan {order_id} (placeholder)")
    return None
