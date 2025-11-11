from __future__ import annotations

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Shared Limiter instance so decorators can be imported without circular issues.
limiter = Limiter(key_func=get_remote_address)

# Custom scopes / utilities can be added here later (e.g., user-specific keys)
