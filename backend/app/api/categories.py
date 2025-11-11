from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.core.security import require_active
from app.schemas.category import CategoryCreate, CategoryRead
from app.models.user import User
from app.services.category_service import list_categories as svc_list_categories, create_category as svc_create_category
from app.core.cache import cache_get_json, cache_set_json, cache_delete

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db_session)):
    # Cache the entire categories list since it is typically small and read-heavy
    key = "categories:list"
    cached = cache_get_json(key)
    if cached is not None:
        return cached
    items = svc_list_categories(db)
    payload = [CategoryRead.model_validate(c).model_dump() for c in items]
    cache_set_json(key, payload, ttl_seconds=120)
    return items


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db_session),
    _user: User = Depends(require_active),
):
    obj = svc_create_category(db, payload)
    # Invalidate categories list cache
    cache_delete("categories:list")
    return obj
