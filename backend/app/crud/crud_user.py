from typing import Optional
from sqlalchemy.orm import Session

from app.models import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_by_email(db: Session, email: str) -> Optional[User]:
	return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: int) -> Optional[User]:
	return db.query(User).filter(User.id == user_id).first()


def create(db: Session, obj_in: UserCreate, hashed_password: str) -> User:
	user = User(
		email=obj_in.email,
		full_name=obj_in.full_name,
		hashed_password=hashed_password,
		is_active=True,
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


# Aliases matching alternative naming used in some snippets
def get_user_by_email(db: Session, email: str) -> Optional[User]:
	return get_by_email(db, email)


def create_user(db: Session, user: UserCreate) -> User:
	"""Create user by hashing password internally."""
	hashed_password = get_password_hash(user.password)
	return create(db, user, hashed_password)

