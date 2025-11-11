from __future__ import annotations

from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.wallet import Wallet, WalletTransaction


def get_or_create_wallet(db: Session, user_id: int) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if wallet:
        return wallet
    wallet = Wallet(user_id=user_id, balance=Decimal("0"))
    db.add(wallet)
    db.flush()  # assign id
    return wallet


def _apply(db: Session, wallet: Wallet, amount: Decimal, tx_type: str, reference: str | None = None) -> WalletTransaction:
    if tx_type == "WITHDRAW" and wallet.balance < amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
    if tx_type == "WITHDRAW":
        wallet.balance -= amount
    else:
        wallet.balance += amount
    tx = WalletTransaction(wallet_id=wallet.id, amount=amount, type=tx_type, reference=reference)
    db.add(tx)
    db.flush()
    return tx


def topup(db: Session, user_id: int, amount: float, reference: str | None = None) -> Wallet:
    wallet = get_or_create_wallet(db, user_id)
    _apply(db, wallet, Decimal(str(amount)), "TOPUP", reference)
    db.commit()
    db.refresh(wallet)
    return wallet


def withdraw(db: Session, user_id: int, amount: float, reference: str | None = None) -> Wallet:
    wallet = get_or_create_wallet(db, user_id)
    _apply(db, wallet, Decimal(str(amount)), "WITHDRAW", reference)
    db.commit()
    db.refresh(wallet)
    return wallet


def list_transactions(db: Session, wallet: Wallet, limit: int = 50):
    return (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet.id)
        .order_by(WalletTransaction.id.desc())
        .limit(limit)
        .all()
    )
