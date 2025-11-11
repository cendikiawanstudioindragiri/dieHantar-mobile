from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(255), unique=True, index=True, nullable=False)
	hashed_password = Column(String(255), nullable=False)
	full_name = Column(String(255), nullable=True)
	phone_number = Column(String(20), nullable=True, index=True)
	is_active = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	# relationships
	# Import dependency note: Location model must be imported somewhere before first use
	locations = relationship("Location", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
	orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
	driver_profile = relationship("Driver", back_populates="user", uselist=False, cascade="all, delete-orphan")
	reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
	wallet = relationship("Wallet", back_populates="user", uselist=False, cascade="all, delete-orphan")