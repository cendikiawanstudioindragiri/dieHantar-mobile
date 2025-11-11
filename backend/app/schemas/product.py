from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ProductBase(BaseModel):
    category_id: int | None = None
    name: str
    description: str | None = None
    price: Decimal
    image_url: str | None = None
    is_available: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    is_available: bool | None = None


class ProductRead(BaseModel):
    id: int
    category_id: int | None = None
    name: str
    description: str | None = None
    price: Decimal
    image_url: str | None = None
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True
