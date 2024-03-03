from typing import Optional
from pydantic import BaseModel


class BaseModel(BaseModel):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ProductBase(BaseModel):
    name: str
    description: str
    company: str
    price: float
    units: int
    subcategory_id: int


class ProductCreate(ProductBase):
    pass


class ProductCreateCSV(ProductBase):
    product_id: int


class ProductUpdate(ProductBase):
    pass


class ProductInDB(ProductBase, BaseModel):
    product_id: int


class Category(BaseModel):
    category_id: int
    name: str


class Subcategory(BaseModel):
    subcategory_id: int
    name: str
    category_id: int
