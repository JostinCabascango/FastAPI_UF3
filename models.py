from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    name: str
    description: str
    company: str
    price: float
    units: int
    subcategory_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class Category(BaseModel):
    category_id: int
    name: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class Subcategory(BaseModel):
    subcategory_id: int
    name: str
    category_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
