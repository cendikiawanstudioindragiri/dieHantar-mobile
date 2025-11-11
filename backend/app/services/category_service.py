from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate
from fastapi import HTTPException, status


def list_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name.asc()).all()


def create_category(db: Session, payload: CategoryCreate) -> Category:
    # Enforce uniqueness at application level to provide a friendly error before DB constraint
    existing = db.query(Category).filter(Category.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")

    obj = Category(name=payload.name, icon_url=payload.icon_url)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
