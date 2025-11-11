"""Aggregate imports for SQLAlchemy models to ensure registry is populated.

Import this package (app.models) to register all model classes before use.
"""
from .user import User  # noqa: F401
from .category import Category  # noqa: F401
from .product import Product  # noqa: F401
from .location import Location  # noqa: F401
from .order import Order  # noqa: F401
from .order_item import OrderItem  # noqa: F401
from .driver import Driver  # noqa: F401
from .payment import Payment  # noqa: F401
from .review import Review  # noqa: F401
from .wallet import Wallet, WalletTransaction  # noqa: F401
from .broadcast import Broadcast, BroadcastStatus  # noqa: F401

__all__ = [
    "User",
    "Category",
    "Product",
    "Location",
    "Order",
    "OrderItem",
    "Driver",
    "Payment",
    "Review",
    "Wallet",
    "WalletTransaction",
    "Broadcast",
    "BroadcastStatus",
]
