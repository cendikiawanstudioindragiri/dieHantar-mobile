from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Review(Base):
	__tablename__ = "reviews"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"))
	product_id = Column(Integer, ForeignKey("products.id"))
	order_id = Column(Integer, ForeignKey("orders.id"))
	driver_id = Column(Integer, ForeignKey("drivers.id"))
	rating = Column(Integer, nullable=False)
	comment = Column(Text, nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	__table_args__ = (
		CheckConstraint('rating >= 1 AND rating <= 5', name='ck_reviews_rating_range'),
	)

	# relationships
	user = relationship("User", back_populates="reviews")
	product = relationship("Product")
	order = relationship("Order", back_populates="reviews")
	driver = relationship("Driver", back_populates="reviews")
