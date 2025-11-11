from __future__ import annotations

from pydantic import BaseModel, Field


class WalletBalance(BaseModel):
    balance: float = 0.0


class WalletTopUpRequest(BaseModel):
    amount: float = Field(gt=0)
    reference: str | None = None


class WalletWithdrawRequest(BaseModel):
    amount: float = Field(gt=0)
    reference: str | None = None


class WalletTransactionRead(BaseModel):
    id: int
    amount: float
    type: str
    reference: str | None
    created_at: str

    class Config:
        from_attributes = True
