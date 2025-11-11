from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.crud import crud_user


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
	existing_user = crud_user.get_user_by_email(db, email=user.email)
	if existing_user:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
	new_user = crud_user.create_user(db, user)
	return new_user
