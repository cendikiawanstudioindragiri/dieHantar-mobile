# blueprints/rides_service.py

from dataclasses import dataclass, asdict
from typing import Optional, Dict
import datetime
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger

logger = get_logger(__name__)
db = get_firestore_client()
RIDES_COLLECTION = 'rides'

class RideStatus(Enum):
    REQUESTED = "requested"       # Pengguna meminta, menunggu driver
    ACCEPTED = "accepted"         # Driver menerima, sedang menuju lokasi jemput
    PICKED_UP = "picked_up"       # Penumpang sudah di dalam kendaraan
    COMPLETED = "completed"       # Perjalanan selesai
    CANCELLED = "cancelled"       # Perjalanan dibatalkan
    NOT_FOUND = "not_found"         # Tidak ada driver yang ditemukan/menerima

@dataclass
class Ride:
    id: str
    user_id: str
    pickup_location: Dict
    destination_location: Dict
    status: str
    vehicle_type: str
    driver_id: Optional[str] = None
    fare: Optional[float] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'Ride':
        return Ride(
            id=doc_id,
            user_id=data.get('user_id'),
            driver_id=data.get('driver_id'),
            pickup_location=data.get('pickup_location'),
            destination_location=data.get('destination_location'),
            status=data.get('status'),
            vehicle_type=data.get('vehicle_type'),
            fare=data.get('fare'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )

    def to_dict(self) -> dict:
        return asdict(self)

def estimate_fare(pickup: Dict, destination: Dict, vehicle: str) -> float:
    # Logika estimasi tarif yang disederhanakan
    # Di dunia nyata, ini akan memanggil layanan pemetaan (misalnya, Google Maps)
    logger.info(f"Estimasi tarif untuk kendaraan {vehicle} dari {pickup} ke {destination}")
    base_fare = {"MOTORCYCLE": 10000, "CAR": 25000}.get(vehicle, 20000)
    # Simulasikan jarak (sangat disederhanakan)
    distance = abs(pickup.get('lat', 0) - destination.get('lat', 0)) + abs(pickup.get('lon', 0) - destination.get('lon', 0))
    estimated_fare = base_fare + (distance * 1500)
    return round(estimated_fare, -2) # Bulatkan ke ratusan terdekat

def request_ride(user_id: str, pickup: Dict, destination: Dict, vehicle: str) -> Ride:
    if not all([pickup, destination, vehicle]):
        raise ValueError("Lokasi jemput, tujuan, dan tipe kendaraan diperlukan.")

    fare = estimate_fare(pickup, destination, vehicle)
    ride_data = {
        'user_id': user_id,
        'pickup_location': pickup,
        'destination_location': destination,
        'vehicle_type': vehicle,
        'status': RideStatus.REQUESTED.value,
        'fare': fare,
        'driver_id': None,
        'created_at': datetime.datetime.utcnow(),
        'updated_at': datetime.datetime.utcnow()
    }
    try:
        ride_ref = db.collection(RIDES_COLLECTION).document()
        ride_ref.set(ride_data)
        logger.info(f"Perjalanan baru {ride_ref.id} diminta oleh pengguna {user_id}")
        return Ride.from_dict(ride_ref.id, ride_data)
    except Exception as e:
        logger.error(f"Gagal membuat permintaan perjalanan di DB: {e}", exc_info=True)
        raise RuntimeError("Gagal menyimpan permintaan perjalanan baru.") from e

def accept_ride_offer(driver_id: str, ride_id: str) -> Ride:
    ride_ref = db.collection(RIDES_COLLECTION).document(ride_id)
    try:
        doc = ride_ref.get()
        if not doc.exists:
            raise ValueError(f"Perjalanan dengan ID {ride_id} tidak ditemukan.")
        
        ride = Ride.from_dict(doc.id, doc.to_dict())
        if ride.status != RideStatus.REQUESTED.value:
            raise PermissionError(f"Perjalanan {ride_id} tidak dalam status 'requested'.")

        update_data = {
            'driver_id': driver_id,
            'status': RideStatus.ACCEPTED.value,
            'updated_at': datetime.datetime.utcnow()
        }
        ride_ref.update(update_data)
        logger.info(f"Driver {driver_id} menerima perjalanan {ride_id}")
        return Ride.from_dict(doc.id, {**doc.to_dict(), **update_data})
    except (ValueError, PermissionError):
        raise # Lemparkan kembali exception yang sudah spesifik
    except Exception as e:
        logger.error(f"Gagal menerima perjalanan {ride_id}: {e}", exc_info=True)
        raise RuntimeError(f"Gagal memperbarui status perjalanan di DB.") from e
