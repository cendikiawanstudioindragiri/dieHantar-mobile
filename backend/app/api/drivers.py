from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.user import User
from ..models.driver import Driver
from ..schemas.driver import (
    DriverAvailabilityUpdate,
    DriverLocationUpdate,
    DriverProfile,
    DriverMetrics
)
from ..services.driver_service import DriverService
from ..core.security import get_current_user

router = APIRouter(prefix="/drivers", tags=["drivers"])

@router.get("/me", response_model=DriverProfile)
async def get_driver_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current driver profile information"""
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver profile not found"
        )
    
    return DriverProfile(
        id=driver.id,
        user_id=driver.user_id,
        vehicle_type=driver.vehicle_type,
        license_plate=driver.license_plate,
        is_active=driver.is_active,
        is_available=driver.is_available,
        rating=driver.rating,
        total_trips=driver.total_trips,
        created_at=driver.created_at,
        last_seen_at=driver.last_seen_at
    )

@router.put("/me/availability", response_model=Dict[str, Any])
async def update_driver_availability(
    availability_update: DriverAvailabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update driver availability status"""
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver profile not found"
        )
    
    if not driver.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver account is not active"
        )
    
    # Update availability using service
    driver_service = DriverService(db)
    updated_driver = await driver_service.update_availability(
        driver_id=driver.id,
        is_available=availability_update.is_available
    )
    
    return {
        "message": "Availability updated successfully",
        "is_available": updated_driver.is_available,
        "updated_at": datetime.utcnow().isoformat()
    }

@router.post("/me/location", response_model=Dict[str, Any])
async def update_driver_location(
    location_update: DriverLocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update driver's current location"""
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver profile not found"
        )
    
    if not driver.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Driver account is not active"
        )
    
    # Update location using service
    driver_service = DriverService(db)
    updated_driver = await driver_service.update_location(
        driver_id=driver.id,
        latitude=location_update.latitude,
        longitude=location_update.longitude
    )
    
    return {
        "message": "Location updated successfully",
        "latitude": updated_driver.last_latitude,
        "longitude": updated_driver.last_longitude,
        "updated_at": updated_driver.last_seen_at.isoformat() if updated_driver.last_seen_at else None
    }

@router.get("/me/metrics", response_model=DriverMetrics)
async def get_driver_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get driver performance metrics"""
    driver = db.query(Driver).filter(Driver.user_id == current_user.id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Driver profile not found"
        )
    
    # Calculate metrics using service
    driver_service = DriverService(db)
    metrics = await driver_service.calculate_metrics(driver_id=driver.id)
    
    return metrics