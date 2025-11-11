from __future__ import annotations

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.broadcast import Broadcast, BroadcastStatus
from app.models.user import User


def create_broadcast(db: Session, title: str, body: str, segment: str, scheduled_at: str | None) -> Broadcast:
    obj = Broadcast(title=title, body=body, segment=segment)
    if scheduled_at:
        try:
            obj.scheduled_at = datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
            obj.status = BroadcastStatus.SCHEDULED
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheduled_at format")
    db.add(obj)
    db.flush()
    return obj


def list_broadcasts(db: Session, limit: int = 50):
    return db.query(Broadcast).order_by(Broadcast.id.desc()).limit(limit).all()


def get_broadcast(db: Session, broadcast_id: int) -> Broadcast:
    obj = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    return obj


def segment_user_query(db: Session, segment: str):
    q = db.query(User)
    if segment == "active":
        q = q.filter(User.is_active.is_(True))
    elif segment == "new":
        # treat users created within last 7 days as new
        window = datetime.utcnow() - timedelta(days=7)
        from sqlalchemy import func
        q = q.filter(User.created_at >= window)
    return q


def preview_segment(db: Session, segment: str) -> int:
    return segment_user_query(db, segment).count()


def send_broadcast(db: Session, broadcast: Broadcast, dry_run: bool = True) -> dict:
    if broadcast.status == BroadcastStatus.SENT:
        raise HTTPException(status_code=400, detail="Already sent")
    # simulate token retrieval (e.g., from user device table). For now we use user count.
    target_count = preview_segment(db, broadcast.segment)
    success = target_count
    failure = 0
    if not dry_run:
        broadcast.mark_sent()
        db.add(broadcast)
    return {
        "id": broadcast.id,
        "status": broadcast.status.value if hasattr(broadcast.status, 'value') else broadcast.status,
        "success": success,
        "failure": failure,
        "dry_run": dry_run,
    }
