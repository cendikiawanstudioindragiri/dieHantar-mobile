from typing import Optional, Mapping, Any
from flask import flash


def flash_dict(category: str, title: Optional[str] = None, body: Optional[str] = None, extra: Optional[Mapping[str, Any]] = None) -> None:
    payload: dict[str, Any] = {}
    if title:
        payload["title"] = title
    if body:
        payload["body"] = body
    if extra:
        payload.update(extra)
    flash(payload if payload else (title or body or ""), category)
