from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from ..models.driver import Driver
from ..models.order import Order
from ..schemas.driver import DriverMetrics


class DriverService:
    def __init__(self, db: Session):
        self.db = db
    
    async def update_availability(self, driver_id: int, is_available: bool) -> Driver:
        """Update driver availability status"""
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise ValueError("Driver not found")
        
        driver.is_available = is_available
        driver.last_seen_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(driver)
        
        return driver
    
    async def update_location(
        self, 
        driver_id: int, 
        latitude: float, 
        longitude: float
    ) -> Driver:
        """Update driver's current location"""
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise ValueError("Driver not found")
        
        driver.last_latitude = latitude
        driver.last_longitude = longitude
        driver.last_seen_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(driver)
        
        return driver
    
    async def calculate_metrics(self, driver_id: int) -> DriverMetrics:
        """Calculate comprehensive driver performance metrics"""
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise ValueError("Driver not found")
        
        # Base metrics from driver model
        total_trips = driver.total_trips or 0
        average_rating = float(driver.rating or 0.0)
        
        # Calculate date ranges
        today = datetime.utcnow().date()
        week_start = today - timedelta(days=today.weekday())
        month_start = today.replace(day=1)
        
        # Query orders for additional metrics
        orders_query = self.db.query(Order).filter(Order.driver_id == driver_id)
        
        # Total earnings calculation
        total_earnings = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            Order.driver_id == driver_id,
            Order.status.in_(['delivered', 'completed'])
        ).scalar() or 0.0
        
        # Weekly metrics
        weekly_orders = orders_query.filter(
            func.date(Order.created_at) >= week_start
        ).count()
        
        weekly_earnings = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            Order.driver_id == driver_id,
            Order.status.in_(['delivered', 'completed']),
            func.date(Order.created_at) >= week_start
        ).scalar() or 0.0
        
        # Monthly metrics
        monthly_orders = orders_query.filter(
            func.date(Order.created_at) >= month_start
        ).count()
        
        monthly_earnings = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            Order.driver_id == driver_id,
            Order.status.in_(['delivered', 'completed']),
            func.date(Order.created_at) >= month_start
        ).scalar() or 0.0
        
        # Daily metrics (today)
        daily_orders = orders_query.filter(
            func.date(Order.created_at) == today
        ).count()
        
        daily_earnings = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            Order.driver_id == driver_id,
            Order.status.in_(['delivered', 'completed']),
            func.date(Order.created_at) == today
        ).scalar() or 0.0
        
        # Acceptance rate (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        total_offers = orders_query.filter(
            func.date(Order.created_at) >= thirty_days_ago
        ).count()
        
        accepted_offers = orders_query.filter(
            func.date(Order.created_at) >= thirty_days_ago,
            Order.status != 'cancelled'
        ).count()
        
        acceptance_rate = (accepted_offers / total_offers * 100) if total_offers > 0 else 0.0
        
        # Completion rate
        total_accepted = orders_query.filter(
            Order.status != 'cancelled'
        ).count()
        
        completed_orders = orders_query.filter(
            Order.status.in_(['delivered', 'completed'])
        ).count()
        
        completion_rate = (completed_orders / total_accepted * 100) if total_accepted > 0 else 0.0
        
        # Calculate average delivery time (in minutes)
        avg_delivery_time_result = self.db.query(
            func.avg(
                func.extract('epoch', Order.delivered_at - Order.created_at) / 60
            )
        ).filter(
            Order.driver_id == driver_id,
            Order.status.in_(['delivered', 'completed']),
            Order.delivered_at.isnot(None)
        ).scalar()
        
        average_delivery_time = float(avg_delivery_time_result or 0.0)
        
        # Online hours calculation (approximate based on last_seen_at updates)
        # This is a simplified calculation - in production, you'd want to track 
        # actual online/offline events
        last_30_days_orders = orders_query.filter(
            func.date(Order.created_at) >= thirty_days_ago
        ).count()
        
        # Estimate 30 minutes online per order (this is a rough estimate)
        estimated_online_hours = last_30_days_orders * 0.5 if last_30_days_orders > 0 else 0.0
        
        return DriverMetrics(
            total_trips=total_trips,
            total_earnings=float(total_earnings),
            average_rating=average_rating,
            acceptance_rate=round(acceptance_rate, 2),
            completion_rate=round(completion_rate, 2),
            average_delivery_time=round(average_delivery_time, 2),
            weekly_orders=weekly_orders,
            weekly_earnings=float(weekly_earnings),
            monthly_orders=monthly_orders,
            monthly_earnings=float(monthly_earnings),
            daily_orders=daily_orders,
            daily_earnings=float(daily_earnings),
            online_hours_this_month=round(estimated_online_hours, 2)
        )
    
    async def get_nearby_drivers(
        self, 
        latitude: float, 
        longitude: float, 
        radius_km: float = 10.0
    ) -> list[Driver]:
        """Get available drivers within specified radius"""
        # Using simplified distance calculation
        # In production, you might want to use PostGIS or more sophisticated geolocation
        drivers = self.db.query(Driver).filter(
            Driver.is_available == True,
            Driver.is_active == True,
            Driver.last_latitude.isnot(None),
            Driver.last_longitude.isnot(None)
        ).all()
        
        nearby_drivers = []
        for driver in drivers:
            if driver.last_latitude and driver.last_longitude:
                # Simple distance calculation (not accurate for large distances)
                lat_diff = abs(driver.last_latitude - latitude)
                lng_diff = abs(driver.last_longitude - longitude)
                
                # Rough approximation: 1 degree ≈ 111 km
                distance_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
                
                if distance_km <= radius_km:
                    nearby_drivers.append(driver)
        
        return nearby_drivers
    
    async def update_driver_rating(
        self, 
        driver_id: int, 
        new_rating: float
    ) -> Driver:
        """Update driver rating based on new order rating"""
        driver = self.db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            raise ValueError("Driver not found")
        
        # Calculate new average rating
        total_trips = driver.total_trips or 0
        current_rating = driver.rating or 0.0
        
        if total_trips == 0:
            driver.rating = new_rating
        else:
            # Weighted average calculation
            total_rating_points = current_rating * total_trips
            new_total_rating_points = total_rating_points + new_rating
            driver.rating = new_total_rating_points / (total_trips + 1)
        
        driver.total_trips = total_trips + 1
        
        self.db.commit()
        self.db.refresh(driver)
        
        return driver