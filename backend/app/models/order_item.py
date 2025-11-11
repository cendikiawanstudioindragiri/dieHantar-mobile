from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.db.session import Base


class OrderItem(Base):
	__tablename__ = "order_items"

	id = Column(Integer, primary_key=True, index=True)
	order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
	product_id = Column(Integer, ForeignKey("products.id"))
	quantity = Column(Integer, nullable=False)
	price_at_time = Column(Numeric(10, 2), nullable=False)

	# relationships
	order = relationship("Order", back_populates="items")
	product = relationship("Product", back_populates="order_items")
