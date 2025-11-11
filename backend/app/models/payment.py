from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship

from app.db.session import Base


class PaymentMethod(str, Enum):
	CASH = "CASH"
	CARD = "CARD"
	QRIS = "QRIS"


class PaymentStatus(str, Enum):
	PENDING = "PENDING"
	SUCCESS = "SUCCESS"
	FAILED = "FAILED"


class Payment(Base):
	__tablename__ = "payments"

	id = Column(Integer, primary_key=True, index=True)
	order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
	method = Column(SAEnum(PaymentMethod, name="payment_method"), nullable=False)
	status = Column(SAEnum(PaymentStatus, name="payment_status"), default=PaymentStatus.PENDING, nullable=False)
	transaction_id = Column(String(255), nullable=True)

	# relationships
	order = relationship("Order", back_populates="payment")
