from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class DriverAvailabilityUpdate(BaseModel):
    is_available: bool


class DriverLocationUpdate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class DriverProfile(BaseModel):
    is_available: bool
    last_latitude: float | None = None
    last_longitude: float | None = None

    class Config:
        from_attributes = True


class DriverMetrics(BaseModel):
    assigned: int
    delivered: int
    cancelled: int
    completion_rate: float
    cancellation_rate: float
