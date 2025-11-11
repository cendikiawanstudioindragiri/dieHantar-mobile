from __future__ import annotations

import json
import logging
import time
from typing import Any, Optional

from app.core.config import settings

try:
	import redis  # type: ignore
except Exception:  # pragma: no cover
	redis = None

logger = logging.getLogger(__name__)

_redis_client = None  # lazy Redis client instance
_local_cache: dict[str, tuple[str, float]] = {}  # key -> (value, expiry_ts)


def get_redis():  # -> Optional[redis.Redis]
	global _redis_client
	if redis is None:
		return None
	if _redis_client is not None:
		return _redis_client
	url = settings.REDIS_URL
	if not url:
		return None
	try:
		_redis_client = redis.from_url(url, decode_responses=True)  # type: ignore
		# ping to validate
		_redis_client.ping()
		return _redis_client
	except Exception as e:  # pragma: no cover
		logger.warning("Redis unavailable: %s", e)
		return None


def cache_get(key: str) -> Optional[str]:
	r = get_redis()
	if r:
		try:
			return r.get(key)
		except Exception:
			return None
	# local fallback
	entry = _local_cache.get(key)
	if not entry:
		return None
	val, exp = entry
	if time.time() > exp:
		_local_cache.pop(key, None)
		return None
	return val


def cache_set(key: str, value: str, ttl_seconds: int) -> None:
	r = get_redis()
	if r:
		try:
			r.setex(key, ttl_seconds, value)
		except Exception:
			pass
		return
	# local fallback
	_local_cache[key] = (value, time.time() + ttl_seconds)


def cache_get_json(key: str) -> Optional[Any]:
	val = cache_get(key)
	if val is None:
		return None
	try:
		return json.loads(val)
	except Exception:
		return None


def cache_set_json(key: str, value: Any, ttl_seconds: int) -> None:
	try:
		cache_set(key, json.dumps(value, default=str), ttl_seconds)
	except Exception:
		pass


def cache_delete(key: str) -> None:
	r = get_redis()
	if r:
		try:
			r.delete(key)
		except Exception:  # pragma: no cover
			pass
	_local_cache.pop(key, None)


def cache_delete_prefix(prefix: str) -> int:
	"""Delete all keys starting with prefix. Returns count deleted.
	Uses SCAN for Redis; linear scan for local fallback.
	"""
	r = get_redis()
	deleted = 0
	if r:
		if not prefix:
			return 0
		try:
			cursor = 0
			pattern = prefix + "*"
			while True:
				cursor, keys = r.scan(cursor=cursor, match=pattern, count=100)
				if keys:
					try:
						deleted += r.delete(*keys)
					except Exception:  # pragma: no cover
						pass
				if cursor == 0:
					break
		except Exception:  # pragma: no cover
			pass
	# local fallback removal
	to_delete = [k for k in _local_cache.keys() if k.startswith(prefix)]
	for k in to_delete:
		_local_cache.pop(k, None)
	deleted += len(to_delete)
	return deleted
