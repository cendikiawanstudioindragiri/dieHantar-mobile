from __future__ import annotations

import json
from pathlib import Path


def load_orders() -> list[dict]:
    here = Path(__file__).parent
    data = json.loads((here / "orders.json").read_text())
    return data


if __name__ == "__main__":
    print(load_orders())
