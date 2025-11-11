from enum import Enum
from sqlalchemy import Column, Integer, Text, DateTime, Numeric, ForeignKey, Enum as SAEnum, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class OrderStatus(str, Enum):
	PENDING = "PENDING"
	CONFIRMED = "CONFIRMED"
	PREPARING = "PREPARING"
	ON_THE_WAY = "ON_THE_WAY"
	DELIVERED = "DELIVERED"
	CANCELLED = "CANCELLED"


class Order(Base):
	__tablename__ = "orders"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
	status = Column(SAEnum(OrderStatus, name="order_status"), default=OrderStatus.PENDING, nullable=False)
	total_amount = Column(Numeric(10, 2), nullable=False)
	delivery_address = Column(Text, nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
	updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

	__table_args__ = (
		Index("idx_orders_user_id", "user_id"),
		Index("idx_orders_status", "status"),
	)

	# relationships
	user = relationship("User", back_populates="orders")
	items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
	payment = relationship("Payment", back_populates="order", uselist=False, cascade="all, delete-orphan")
	reviews = relationship("Review", back_populates="order", cascade="all, delete-orphan")
