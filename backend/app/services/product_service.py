from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException

from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate


def list_products(db: Session, skip: int = 0, limit: int = 20, available: bool | None = None, category_id: int | None = None) -> list[Product]:
    query = db.query(Product).options(selectinload(Product.category))
    if available is not None:
        query = query.filter(Product.is_available == available)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)
    return query.order_by(Product.created_at.desc()).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Product | None:
    return (
        db.query(Product)
        .options(selectinload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )


def create_product(db: Session, payload: ProductCreate) -> Product:
    if payload.category_id is not None:
        category = db.query(Category).filter(Category.id == payload.category_id).first()
        if category is None:
            raise HTTPException(status_code=400, detail="Category not found")

    obj = Product(
        category_id=payload.category_id,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        image_url=payload.image_url,
        is_available=payload.is_available,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    data = payload.model_dump(exclude_unset=True)

    if "category_id" in data and data["category_id"] is not None:
        cat = db.query(Category).filter(Category.id == data["category_id"]).first()
        if cat is None:
            raise HTTPException(status_code=400, detail="Category not found")

    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return None
