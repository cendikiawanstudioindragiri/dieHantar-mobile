from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User


def get_db_session(db: Session = Depends(get_db)) -> Session:
	"""Expose DB session as a dependency alias for route modules."""
	return db


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
	"""Ensure the authenticated user is active."""
	if not current_user.is_active:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user",
		)
	return current_user
