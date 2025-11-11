from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.wallet import (
    WalletBalance,
    WalletTopUpRequest,
    WalletWithdrawRequest,
    WalletTransactionRead,
)
from app.core.security import require_active
from app.models.user import User
from app.services.wallet_service import get_or_create_wallet, topup as svc_topup, withdraw as svc_withdraw, list_transactions


router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("/balance", response_model=WalletBalance)
def balance(db: Session = Depends(get_db), user: User = Depends(require_active)):
    wallet = get_or_create_wallet(db, user.id)
    return {"balance": float(wallet.balance or 0)}


@router.get("/transactions", response_model=list[WalletTransactionRead])
def transactions(db: Session = Depends(get_db), user: User = Depends(require_active)):
    wallet = get_or_create_wallet(db, user.id)
    items = list_transactions(db, wallet)
    # Pydantic will convert from ORM via from_attributes, but also ensure float for amount
    out = []
    for tx in items:
        out.append(
            WalletTransactionRead(
                id=tx.id,
                amount=float(tx.amount),
                type=tx.type,
                reference=tx.reference,
                created_at=tx.created_at.isoformat() if getattr(tx, "created_at", None) else None,
            )
        )
    return out


@router.post("/topup", response_model=WalletBalance, status_code=status.HTTP_201_CREATED)
def topup(payload: WalletTopUpRequest, db: Session = Depends(get_db), user: User = Depends(require_active)):
    wallet = svc_topup(db, user.id, payload.amount, payload.reference)
    return {"balance": float(wallet.balance)}


@router.post("/withdraw", response_model=WalletBalance)
def withdraw(payload: WalletWithdrawRequest, db: Session = Depends(get_db), user: User = Depends(require_active)):
    wallet = svc_withdraw(db, user.id, payload.amount, payload.reference)
    return {"balance": float(wallet.balance)}
