from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json
import hashlib
from pydantic import BaseModel, Field

from app.api.deps import get_db_session, get_current_active_user
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.models.user import User
from app.services.product_service import (
    list_products as svc_list_products,
    get_product as svc_get_product,
    create_product as svc_create_product,
    update_product as svc_update_product,
    delete_product as svc_delete_product,
)
from app.core.cache import cache_get_json, cache_set_json, cache_delete_prefix

router = APIRouter(prefix="/products", tags=["products"])


class ProductListParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)
    available: bool | None = None
    category_id: int | None = None


def build_products_query(db: Session, params: ProductListParams):
    # retained for compatibility; not used directly after service refactor
    return db


@router.get("/", response_model=list[ProductRead])
def list_products(
    params: ProductListParams = Depends(),
    db: Session = Depends(get_db_session),
):
    # Try cache first
    cache_key = "products:list:" + hashlib.sha256(json.dumps(params.model_dump(), sort_keys=True).encode()).hexdigest()
    cached = cache_get_json(cache_key)
    if cached is not None:
        return cached
    items = svc_list_products(db, skip=params.skip, limit=params.limit, available=params.available, category_id=params.category_id)
    # serialize via pydantic to ensure JSON-able types
    from app.schemas.product import ProductRead
    payload = [ProductRead.model_validate(i).model_dump() for i in items]
    cache_set_json(cache_key, payload, ttl_seconds=60)
    return items


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db_session)):
    product = svc_get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_active_user),
):
    obj = svc_create_product(db, payload)
    # Invalidate cached product lists (any filter combinations) after mutation
    cache_delete_prefix("products:list:")
    return obj


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_active_user),
):
    obj = svc_update_product(db, product_id, payload)
    cache_delete_prefix("products:list:")
    return obj


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db_session),
    _: User = Depends(get_current_active_user),
):
    svc_delete_product(db, product_id)
    cache_delete_prefix("products:list:")
    return None
