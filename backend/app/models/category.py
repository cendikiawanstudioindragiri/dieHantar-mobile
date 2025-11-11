from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Category(Base):
	__tablename__ = "categories"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), nullable=False)
	icon_url = Column(String(255), nullable=True)
	created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	# relationships
	products = relationship("Product", back_populates="category")
