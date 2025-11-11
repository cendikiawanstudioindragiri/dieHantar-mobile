from datetime import datetime
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    icon_url: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
