from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PricingInput:
    distance_km: float
    base_fare: float = 2.0
    per_km: float = 0.8


def estimate_price(inp: PricingInput) -> float:
    distance = max(0.0, float(inp.distance_km))
    price = inp.base_fare + inp.per_km * distance
    return round(price, 2)
