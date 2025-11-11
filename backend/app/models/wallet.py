from __future__ import annotations

from decimal import Decimal
from sqlalchemy import Column, Integer, Numeric, ForeignKey, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    balance = Column(Numeric(12, 2), nullable=False, default=0)

    user = relationship("User", back_populates="wallet", uselist=False)
    transactions = relationship("WalletTransaction", back_populates="wallet", cascade="all, delete-orphan")


class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    type = Column(String(20), nullable=False)  # TOPUP | WITHDRAW | ADJUST
    reference = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    wallet = relationship("Wallet", back_populates="transactions")
