from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Location(Base):
	__tablename__ = "locations"

	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
	name = Column(String(100), nullable=False)
	address = Column(Text, nullable=False)
	latitude = Column(Numeric(10, 8), nullable=True)
	longitude = Column(Numeric(11, 8), nullable=True)
	is_favorite = Column(Boolean, default=False, nullable=False)

	# relationships
	user = relationship("User", back_populates="locations")
