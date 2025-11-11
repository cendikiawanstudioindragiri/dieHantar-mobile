from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import require_active
from app.models.user import User
from app.schemas.broadcast import (
    BroadcastCreate,
    BroadcastRead,
    BroadcastSendRequest,
    BroadcastSendResult,
)
from app.services.broadcast_service import (
    create_broadcast,
    list_broadcasts,
    get_broadcast,
    preview_segment,
    send_broadcast,
)


router = APIRouter(prefix="/admin/broadcasts", tags=["admin-broadcasts"])


@router.post("/", response_model=BroadcastRead, status_code=status.HTTP_201_CREATED)
def create(payload: BroadcastCreate, db: Session = Depends(get_db), _admin: User = Depends(require_active)):
    obj = create_broadcast(db, payload.title, payload.body, payload.segment, payload.scheduled_at)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[BroadcastRead])
def list_items(db: Session = Depends(get_db), _admin: User = Depends(require_active)):
    return list_broadcasts(db)


@router.get("/{broadcast_id}/preview")
def preview(broadcast_id: int, db: Session = Depends(get_db), _admin: User = Depends(require_active)):
    obj = get_broadcast(db, broadcast_id)
    size = preview_segment(db, obj.segment)
    return {"id": obj.id, "segment": obj.segment, "estimated_targets": size}


@router.post("/{broadcast_id}/send", response_model=BroadcastSendResult)
def send(broadcast_id: int, payload: BroadcastSendRequest, db: Session = Depends(get_db), _admin: User = Depends(require_active)):
    obj = get_broadcast(db, broadcast_id)
    result = send_broadcast(db, obj, dry_run=payload.dry_run)
    return result
