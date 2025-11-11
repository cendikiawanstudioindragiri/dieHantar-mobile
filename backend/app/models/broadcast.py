from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Text
from sqlalchemy.sql import func
from enum import Enum

from app.db.session import Base


class BroadcastStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    SENT = "SENT"


class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    segment = Column(String(50), nullable=False, default="all")  # all|active|new
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(SAEnum(BroadcastStatus, name="broadcast_status"), nullable=False, default=BroadcastStatus.DRAFT)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def mark_sent(self):  # simple state transition
        self.status = BroadcastStatus.SENT
        self.sent_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
