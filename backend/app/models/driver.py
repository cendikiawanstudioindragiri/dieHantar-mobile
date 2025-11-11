from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class Driver(Base):
	__tablename__ = "drivers"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
	license_plate = Column(String(20), nullable=True)
	vehicle_type = Column(String(50), nullable=True)
	is_available = Column(Boolean, default=True, nullable=False)
	# last known location / heartbeat
	last_latitude = Column(Numeric(10, 8), nullable=True)
	last_longitude = Column(Numeric(11, 8), nullable=True)
	last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

	__table_args__ = (
		Index("idx_drivers_user_id", "user_id"),
	)

	# relationships
	user = relationship("User", back_populates="driver_profile")
	reviews = relationship("Review", back_populates="driver")
