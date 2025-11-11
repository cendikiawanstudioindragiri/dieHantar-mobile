from __future__ import annotations

import json
import logging
import os
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # type: ignore[override]
        payload: dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging() -> None:
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)

    use_json = os.getenv("FLASK_LOG_JSON", "0") == "1"
    level = logging.DEBUG if os.getenv("FLASK_ENV", "development") == "development" else logging.INFO

    handler = logging.StreamHandler()
    handler.setLevel(level)
    if use_json:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))

    root.setLevel(level)
    root.addHandler(handler)
