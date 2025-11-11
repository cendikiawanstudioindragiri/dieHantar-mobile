from fastapi import APIRouter, Depends
import json, hashlib
from app.core.security import get_current_user
from app.core.cache import cache_get_json, cache_set_json
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/me", tags=["auth"])


@router.get("", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
	# cache user profile for short TTL (avoid repeated DB hits on high-frequency polling)
	key = "me:user:" + hashlib.sha256(str(current_user.id).encode()).hexdigest()
	cached = cache_get_json(key)
	if cached:
		return cached
	data = UserRead.model_validate(current_user).model_dump()
	cache_set_json(key, data, ttl_seconds=30)
	return current_user