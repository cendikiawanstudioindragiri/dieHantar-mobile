import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.models.user import User
from app.models.driver import Driver
from app.models.order import Order
from app.core.security import create_access_token


def create_driver_user_and_auth_headers(client: TestClient, db: Session):
    """Helper to create a driver user and return auth headers"""
    # Create user via API
    signup_data = {
        "email": "driver@example.com", 
        "password": "Secret123", 
        "full_name": "Test Driver"
    }
    client.post("/auth/signup", json=signup_data)
    
    # Login to get token
    r = client.post("/auth/login", json={
        "email": "driver@example.com", 
        "password": "Secret123"
    })
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get the user from database
    user = db.query(User).filter(User.email == "driver@example.com").first()
    
    # Create driver profile
    driver = Driver(
        user_id=user.id,
        vehicle_type="motorcycle",
        license_plate="B1234XYZ",
        is_active=True,
        is_available=False,
        rating=4.5,
        total_trips=25,
        last_latitude=-6.2088,
        last_longitude=106.8456,
        last_seen_at=datetime.utcnow()
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)
    
    return user, driver, headers


class TestDriverEndpoints:
    """Test suite for driver-related endpoints"""

    def test_get_driver_profile_success(self, client: TestClient, db: Session):
        """Test successful retrieval of driver profile"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        response = client.get("/drivers/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == driver.id
        assert data["user_id"] == driver.user_id
        assert data["vehicle_type"] == "motorcycle"
        assert data["license_plate"] == "B1234XYZ"
        assert data["is_active"] is True
        assert data["is_available"] is False
        assert data["rating"] == 4.5
        assert data["total_trips"] == 25

    def test_get_driver_profile_not_found(self, client: TestClient, db: Session):
        """Test driver profile not found"""
        # Create user without driver profile
        signup_data = {
            "email": "nodriver@example.com", 
            "password": "Secret123", 
            "full_name": "No Driver"
        }
        client.post("/auth/signup", json=signup_data)
        
        r = client.post("/auth/login", json={
            "email": "nodriver@example.com", 
            "password": "Secret123"
        })
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        response = client.get("/drivers/me", headers=headers)
        
        assert response.status_code == 404
        assert "Driver profile not found" in response.json()["detail"]

    def test_update_availability_success(self, client: TestClient, db: Session):
        """Test successful availability update"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        update_data = {"is_available": True}
        
        response = client.put("/drivers/me/availability", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "Availability updated successfully"
        assert data["is_available"] is True
        assert "updated_at" in data

    def test_update_availability_inactive_driver(self, client: TestClient, db: Session):
        """Test availability update for inactive driver"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        # Make driver inactive
        driver.is_active = False
        db.commit()
        
        update_data = {"is_available": True}
        
        response = client.put("/drivers/me/availability", json=update_data, headers=headers)
        
        assert response.status_code == 403
        assert "Driver account is not active" in response.json()["detail"]

    def test_update_location_success(self, client: TestClient, db: Session):
        """Test successful location update"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        update_data = {
            "latitude": -6.2144,
            "longitude": 106.8451
        }
        
        response = client.post("/drivers/me/location", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["message"] == "Location updated successfully"
        assert data["latitude"] == -6.2144
        assert data["longitude"] == 106.8451
        assert "updated_at" in data

    def test_update_location_inactive_driver(self, client: TestClient, db: Session):
        """Test location update for inactive driver"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        # Make driver inactive
        driver.is_active = False
        db.commit()
        
        update_data = {
            "latitude": -6.2144,
            "longitude": 106.8451
        }
        
        response = client.post("/drivers/me/location", json=update_data, headers=headers)
        
        assert response.status_code == 403
        assert "Driver account is not active" in response.json()["detail"]

    def test_get_driver_metrics_success(self, client: TestClient, db: Session):
        """Test successful retrieval of driver metrics"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        # Create some test orders for metrics calculation
        today = datetime.utcnow()
        
        # Create completed orders for earnings calculation
        for i in range(3):
            order = Order(
                driver_id=driver.id,
                user_id=user.id,
                status="delivered",
                total_amount=50000.0 + (i * 10000),
                created_at=today - timedelta(days=i),
                delivered_at=today - timedelta(days=i, hours=-1)
            )
            db.add(order)
        
        db.commit()
        
        response = client.get("/drivers/me/metrics", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Check basic metrics
        assert data["total_trips"] == driver.total_trips
        assert data["average_rating"] == driver.rating
        assert data["total_earnings"] > 0
        assert "acceptance_rate" in data
        assert "completion_rate" in data

    def test_get_driver_metrics_no_orders(self, client: TestClient, db: Session):
        """Test driver metrics with no order history"""
        user, driver, headers = create_driver_user_and_auth_headers(client, db)
        
        response = client.get("/drivers/me/metrics", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return zero metrics for driver with no orders
        assert data["total_trips"] == driver.total_trips
        assert data["average_rating"] == driver.rating
        assert data["total_earnings"] == 0.0
        assert data["weekly_orders"] == 0
        assert data["monthly_orders"] == 0

    def test_driver_endpoints_unauthorized(self, client: TestClient):
        """Test all driver endpoints without authentication"""
        endpoints = [
            ("GET", "/drivers/me"),
            ("PUT", "/drivers/me/availability"),
            ("POST", "/drivers/me/location"),
            ("GET", "/drivers/me/metrics"),
        ]
        
        for method, endpoint in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            elif method == "PUT":
                response = client.put(endpoint, json={})
            elif method == "POST":
                response = client.post(endpoint, json={})
            
            assert response.status_code == 401