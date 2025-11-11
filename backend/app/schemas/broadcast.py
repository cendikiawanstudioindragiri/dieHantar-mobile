from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal


class BroadcastCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    segment: Literal["all", "active", "new"] = "all"
    scheduled_at: str | None = None


class BroadcastRead(BaseModel):
    id: int
    title: str
    body: str
    segment: str
    status: str
    scheduled_at: str | None = None
    sent_at: str | None = None

    class Config:
        from_attributes = True


class BroadcastSendRequest(BaseModel):
    dry_run: bool = True
    tokens: list[str] = []


class BroadcastSendResult(BaseModel):
    id: int
    status: str
    success: int
    failure: int
    dry_run: bool
