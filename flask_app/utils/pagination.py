from __future__ import annotations

from math import ceil


def paginate(query, page: int = 1, per_page: int = 20):
    page = max(page, 1)
    per_page = max(per_page, 1)
    total = query.count()
    items = query.limit(per_page).offset((page - 1) * per_page).all()
    pages = ceil(total / per_page) if per_page else 0
    return {
        "items": items,
        "meta": {"page": page, "per_page": per_page, "total": total, "pages": pages},
    }
