from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Product(Base):
	__tablename__ = "products"

	id = Column(Integer, primary_key=True, index=True)
	category_id = Column(Integer, ForeignKey("categories.id"))
	name = Column(String(255), nullable=False)
	description = Column(Text, nullable=True)
	price = Column(Numeric(10, 2), nullable=False)
	image_url = Column(String(255), nullable=True)
	is_available = Column(Boolean, default=True, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	__table_args__ = (
		Index("idx_products_category_id", "category_id"),
	)

	# relationships
	category = relationship("Category", back_populates="products")
	order_items = relationship("OrderItem", back_populates="product")
