# blueprints/drivers_service.py

from dataclasses import dataclass, asdict
from typing import Optional, Dict, List, Tuple
import datetime
import math
from enum import Enum
from firebase_config import get_firestore_client
from logger_config import get_logger
from geopy.distance import geodesic
import googlemaps
import os

logger = get_logger(__name__)
db = get_firestore_client()
DRIVERS_COLLECTION = 'drivers'

# Initialize Google Maps client (optional, untuk routing yang lebih akurat)
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
gmaps_client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else None

class DriverStatus(Enum):
    OFFLINE = "offline"
    ONLINE = "online"      # Tersedia untuk menerima pesanan
    BUSY = "busy"          # Sedang dalam perjalanan atau menangani pesanan
    EN_ROUTE = "en_route"  # Dalam perjalanan ke lokasi pickup/delivery

@dataclass
class LocationUpdate:
    lat: float
    lon: float
    timestamp: datetime.datetime
    accuracy: Optional[float] = None  # GPS accuracy in meters
    speed: Optional[float] = None     # Speed in km/h
    heading: Optional[float] = None   # Direction in degrees (0-360)

@dataclass  
class Driver:
    id: str
    name: str
    vehicle_type: str # e.g., 'MOTORCYCLE', 'CAR'
    status: str
    current_location: Optional[Dict] = None
    location_history: Optional[List[Dict]] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    is_online: Optional[bool] = None
    last_seen: Optional[datetime.datetime] = None

    @staticmethod
    def from_dict(doc_id: str, data: dict) -> 'Driver':
        return Driver(
            id=doc_id,
            name=data.get('name'),
            vehicle_type=data.get('vehicle_type'),
            status=data.get('status'),
            current_location=data.get('current_location'),
            location_history=data.get('location_history', []),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            is_online=data.get('is_online', False),
            last_seen=data.get('last_seen')
        )

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class NearbyDriver:
    driver: Driver
    distance_km: float
    estimated_arrival_time: int  # in minutes
    
    def to_dict(self) -> dict:
        return {
            'driver': self.driver.to_dict(),
            'distance_km': round(self.distance_km, 2),
            'estimated_arrival_time': self.estimated_arrival_time
        }

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Hitung jarak antara dua titik koordinat menggunakan Haversine formula.
    
    Args:
        lat1, lon1: Koordinat titik pertama
        lat2, lon2: Koordinat titik kedua
    
    Returns:
        float: Jarak dalam kilometer
    """
    try:
        # Gunakan geopy jika tersedia, fallback ke Haversine manual
        if 'geodesic' in globals():
            return geodesic((lat1, lon1), (lat2, lon2)).kilometers
        else:
            # Haversine formula manual
            R = 6371  # Radius bumi dalam km
            
            # Convert to radians
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return R * c
    except Exception as e:
        logger.error(f"Error calculating distance: {e}")
        return 0.0

def estimate_travel_time(distance_km: float, vehicle_type: str) -> int:
    """
    Estimasi waktu tempuh berdasarkan jarak dan jenis kendaraan.
    
    Args:
        distance_km: Jarak dalam kilometer
        vehicle_type: Jenis kendaraan ('MOTORCYCLE', 'CAR')
    
    Returns:
        int: Estimasi waktu dalam menit
    """
    # Kecepatan rata-rata dalam kondisi traffic normal (km/h)
    avg_speeds = {
        'MOTORCYCLE': 25,  # Motor lebih cepat di traffic
        'CAR': 20,         # Mobil lebih lambat di traffic
        'BICYCLE': 15      # Sepeda
    }
    
    speed = avg_speeds.get(vehicle_type.upper(), 20)
    time_hours = distance_km / speed
    time_minutes = time_hours * 60
    
    # Minimal 2 menit, maksimal 120 menit
    return max(2, min(120, int(time_minutes)))

def get_route_info(origin_lat: float, origin_lon: float, 
                  dest_lat: float, dest_lon: float) -> Dict:
    """
    Dapatkan informasi rute menggunakan Google Maps API (jika tersedia).
    
    Returns:
        Dict: Informasi rute dengan distance, duration, dan polyline
    """
    try:
        if gmaps_client:
            # Gunakan Google Maps API untuk akurasi tinggi
            directions = gmaps_client.directions(
                origin=(origin_lat, origin_lon),
                destination=(dest_lat, dest_lon),
                mode="driving",
                departure_time=datetime.datetime.now(),
                traffic_model="best_guess"
            )
            
            if directions:
                route = directions[0]['legs'][0]
                return {
                    'distance_km': route['distance']['value'] / 1000,
                    'duration_minutes': route['duration']['value'] / 60,
                    'duration_in_traffic_minutes': route.get('duration_in_traffic', {}).get('value', 0) / 60,
                    'polyline': directions[0]['overview_polyline']['points'],
                    'start_address': route['start_address'],
                    'end_address': route['end_address']
                }
        
        # Fallback ke perhitungan manual
        distance = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        duration = estimate_travel_time(distance, 'CAR')
        
        return {
            'distance_km': distance,
            'duration_minutes': duration,
            'duration_in_traffic_minutes': duration * 1.2,  # Asumsi traffic 20% lebih lama
            'polyline': None,
            'start_address': f"{origin_lat:.6f}, {origin_lon:.6f}",
            'end_address': f"{dest_lat:.6f}, {dest_lon:.6f}"
        }
        
    except Exception as e:
        logger.error(f"Error getting route info: {e}", exc_info=True)
        # Return basic calculation as fallback
        distance = calculate_distance(origin_lat, origin_lon, dest_lat, dest_lon)
        return {
            'distance_km': distance,
            'duration_minutes': estimate_travel_time(distance, 'CAR'),
            'duration_in_traffic_minutes': estimate_travel_time(distance, 'CAR') * 1.3,
            'polyline': None,
            'start_address': f"{origin_lat:.6f}, {origin_lon:.6f}",
            'end_address': f"{dest_lat:.6f}, {dest_lon:.6f}"
        }

def get_driver_public_info(driver_id: str) -> Driver:
    """Dapatkan informasi publik driver (untuk ditampilkan ke customer)."""
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

def update_driver_location(driver_id: str, lat: float, lon: float, 
                          accuracy: Optional[float] = None,
                          speed: Optional[float] = None,
                          heading: Optional[float] = None) -> None:
    """
    Update lokasi driver dengan informasi tambahan untuk real-time tracking.
    
    Args:
        driver_id: ID driver
        lat, lon: Koordinat lokasi
        accuracy: Akurasi GPS dalam meter (optional)
        speed: Kecepatan dalam km/h (optional)  
        heading: Arah hadap dalam derajat 0-360 (optional)
    """
    if not all([driver_id, isinstance(lat, (int, float)), isinstance(lon, (int, float))]):
        raise ValueError("ID Driver, latitude, dan longitude diperlukan dan harus berupa angka.")
    
    # Validasi koordinat
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Koordinat tidak valid. Latitude: -90 to 90, Longitude: -180 to 180")
    
    now = datetime.datetime.utcnow()
    
    # Buat location update object
    location_update = LocationUpdate(
        lat=lat,
        lon=lon,
        timestamp=now,
        accuracy=accuracy,
        speed=speed,
        heading=heading
    )
    
    try:
        doc_ref = db.collection(DRIVERS_COLLECTION).document(driver_id)
        
        # Ambil data driver saat ini untuk history
        current_doc = doc_ref.get()
        location_history = []
        
        if current_doc.exists:
            current_data = current_doc.to_dict()
            location_history = current_data.get('location_history', [])
            
            # Batasi history ke 50 lokasi terakhir untuk menghemat storage
            if len(location_history) >= 50:
                location_history = location_history[-49:]  # Keep last 49, add 1 new
        
        # Tambah lokasi baru ke history
        location_history.append(asdict(location_update))
        
        # Update data lengkap
        location_data = {
            'current_location': {
                'lat': lat, 
                'lon': lon,
                'accuracy': accuracy,
                'speed': speed,
                'heading': heading,
                'updated_at': now
            },
            'location_history': location_history,
            'updated_at': now,
            'last_seen': now,
            'is_online': True  # Assume online jika kirim lokasi
        }
        
        # Gunakan merge=True untuk membuat dokumen jika belum ada, atau memperbarui jika sudah ada
        doc_ref.set(location_data, merge=True)
        logger.info(f"Lokasi driver {driver_id} diperbarui ke ({lat}, {lon}) dengan akurasi {accuracy}m")
        
    except Exception as e:
        logger.error(f"Gagal memperbarui lokasi driver {driver_id}: {e}", exc_info=True)
        raise RuntimeError("Gagal memperbarui lokasi driver di database.") from e

def find_nearby_drivers(pickup_lat: float, pickup_lon: float, 
                       max_distance_km: float = 10.0,
                       vehicle_type: Optional[str] = None,
                       limit: int = 10) -> List[NearbyDriver]:
    """
    Cari driver terdekat berdasarkan lokasi pickup.
    
    Args:
        pickup_lat, pickup_lon: Koordinat lokasi pickup
        max_distance_km: Jarak maksimal pencarian dalam km
        vehicle_type: Filter berdasarkan jenis kendaraan (optional)
        limit: Maksimal jumlah driver yang dikembalikan
    
    Returns:
        List[NearbyDriver]: Daftar driver terdekat beserta jarak dan ETA
    """
    try:
        # Query driver yang online dan tidak busy
        drivers_query = db.collection(DRIVERS_COLLECTION)\
            .where('status', 'in', ['online', DriverStatus.ONLINE.value])\
            .where('is_online', '==', True)
        
        if vehicle_type:
            drivers_query = drivers_query.where('vehicle_type', '==', vehicle_type.upper())
            
        # Batasi query untuk performa
        drivers_query = drivers_query.limit(50)
        
        nearby_drivers = []
        
        for doc in drivers_query.get():
            driver_data = doc.to_dict()
            current_location = driver_data.get('current_location')
            
            if not current_location or 'lat' not in current_location or 'lon' not in current_location:
                continue
                
            # Hitung jarak
            driver_lat = current_location['lat']
            driver_lon = current_location['lon']
            distance = calculate_distance(pickup_lat, pickup_lon, driver_lat, driver_lon)
            
            # Filter berdasarkan jarak maksimal
            if distance <= max_distance_km:
                # Estimasi waktu kedatangan
                eta_minutes = estimate_travel_time(distance, driver_data.get('vehicle_type', 'CAR'))
                
                # Buat object driver
                driver = Driver.from_dict(doc.id, driver_data)
                
                # Tambah ke list
                nearby_drivers.append(NearbyDriver(
                    driver=driver,
                    distance_km=distance,
                    estimated_arrival_time=eta_minutes
                ))
        
        # Sort berdasarkan jarak terdekat
        nearby_drivers.sort(key=lambda x: x.distance_km)
        
        # Return sesuai limit
        return nearby_drivers[:limit]
        
    except Exception as e:
        logger.error(f"Error finding nearby drivers: {e}", exc_info=True)
        return []

def find_and_assign_nearest_driver(order_id: str, pickup_location: Dict, 
                                  vehicle_preference: str = None) -> Optional[str]:
    """
    Cari dan assign driver terdekat untuk pesanan.
    
    Args:
        order_id: ID pesanan
        pickup_location: Lokasi pickup {'lat': float, 'lon': float}
        vehicle_preference: Preferensi jenis kendaraan
    
    Returns:
        str: Driver ID yang di-assign, atau None jika tidak ditemukan
    """
    try:
        pickup_lat = pickup_location.get('lat')
        pickup_lon = pickup_location.get('lon')
        
        if not pickup_lat or not pickup_lon:
            logger.error(f"Invalid pickup location for order {order_id}: {pickup_location}")
            return None
            
        # Cari driver terdekat
        nearby_drivers = find_nearby_drivers(
            pickup_lat=pickup_lat,
            pickup_lon=pickup_lon,
            max_distance_km=15.0,  # 15km radius
            vehicle_type=vehicle_preference,
            limit=5  # Top 5 terdekat
        )
        
        if not nearby_drivers:
            logger.warning(f"No available drivers found for order {order_id}")
            return None
            
        # Pilih driver terdekat (index 0)
        selected_driver = nearby_drivers[0].driver
        
        # Update status driver menjadi BUSY
        driver_ref = db.collection(DRIVERS_COLLECTION).document(selected_driver.id)
        driver_ref.update({
            'status': DriverStatus.BUSY.value,
            'current_order_id': order_id,
            'updated_at': datetime.datetime.utcnow()
        })
        
        logger.info(f"Driver {selected_driver.id} assigned to order {order_id}")
        return selected_driver.id
        
    except Exception as e:
        logger.error(f"Error assigning driver to order {order_id}: {e}", exc_info=True)
        return None

def update_driver_status(driver_id: str, new_status: str, order_id: Optional[str] = None) -> None:
    """
    Update status driver.
    
    Args:
        driver_id: ID driver
        new_status: Status baru (online, busy, offline, en_route)
        order_id: ID pesanan terkait (optional)
    """
    try:
        # Validasi status
        valid_statuses = [status.value for status in DriverStatus]
        if new_status not in valid_statuses:
            raise ValueError(f"Status tidak valid: {new_status}. Yang valid: {valid_statuses}")
            
        update_data = {
            'status': new_status,
            'updated_at': datetime.datetime.utcnow()
        }
        
        # Jika ada order_id, simpan referensinya
        if order_id:
            update_data['current_order_id'] = order_id
        elif new_status in ['online', 'offline']:
            # Clear current order jika status kembali online/offline
            update_data['current_order_id'] = None
            
        # Update di database
        doc_ref = db.collection(DRIVERS_COLLECTION).document(driver_id)
        doc_ref.update(update_data)
        
        logger.info(f"Driver {driver_id} status updated to {new_status}")
        
    except Exception as e:
        logger.error(f"Error updating driver status for {driver_id}: {e}", exc_info=True)
        raise RuntimeError(f"Gagal update status driver: {str(e)}") from e

def get_driver_location_history(driver_id: str, limit: int = 20) -> List[Dict]:
    """
    Ambil riwayat lokasi driver untuk tracking.
    
    Args:
        driver_id: ID driver
        limit: Maksimal history yang dikembalikan
    
    Returns:
        List[Dict]: History lokasi driver
    """
    try:
        doc_ref = db.collection(DRIVERS_COLLECTION).document(driver_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            return []
            
        driver_data = doc.to_dict()
        location_history = driver_data.get('location_history', [])
        
        # Return history terakhir sesuai limit
        return location_history[-limit:] if location_history else []
        
    except Exception as e:
        logger.error(f"Error getting location history for driver {driver_id}: {e}", exc_info=True)
        return []

def calculate_driver_eta(driver_id: str, destination_lat: float, destination_lon: float) -> Optional[Dict]:
    """
    Hitung ETA driver ke lokasi tujuan berdasarkan lokasi terkini.
    
    Args:
        driver_id: ID driver
        destination_lat, destination_lon: Koordinat tujuan
    
    Returns:
        Dict: Informasi ETA dan rute, atau None jika tidak bisa dihitung
    """
    try:
        # Ambil lokasi driver saat ini
        driver = get_driver_public_info(driver_id)
        
        if not driver.current_location:
            return None
            
        driver_lat = driver.current_location.get('lat')
        driver_lon = driver.current_location.get('lon')
        
        if not driver_lat or not driver_lon:
            return None
            
        # Dapatkan informasi rute
        route_info = get_route_info(driver_lat, driver_lon, destination_lat, destination_lon)
        
        return {
            'driver_id': driver_id,
            'current_location': {'lat': driver_lat, 'lon': driver_lon},
            'destination': {'lat': destination_lat, 'lon': destination_lon},
            'distance_km': route_info['distance_km'],
            'eta_minutes': int(route_info['duration_in_traffic_minutes']),
            'route_polyline': route_info.get('polyline'),
            'calculated_at': datetime.datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating ETA for driver {driver_id}: {e}", exc_info=True)
        return None
