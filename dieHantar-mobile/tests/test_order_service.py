# tests/test_order_service.py

import pytest
from blueprints.order_service import calculate_order_summary


def test_calculate_order_summary():
    items = [
        {"id": "f1", "price": 25000, "qty": 2, "category": "foods"},
        {"id": "d1", "price": 5000, "qty": 1, "category": "drinks"}
    ]

    summary = calculate_order_summary(items)

    assert summary["subtotal"] == 55000
    assert summary["shipping_cost"] == 15000
    assert summary["total_amount"] == 70000
