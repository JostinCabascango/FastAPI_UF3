from typing import Optional
from pydantic import BaseModel


class BaseModelTimestamp(BaseModel):
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ProductBase(BaseModelTimestamp):
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


class ProductInDB(ProductBase, BaseModelTimestamp):
    product_id: int


class Category(BaseModelTimestamp):
    category_id: int
    name: str


class Subcategory(BaseModelTimestamp):
    subcategory_id: int
    name: str
    category_id: int


class ProductSubcategoryCategory(BaseModel):
    category_name: str
    subcategory_name: str
    product_name: str
    product_brand: str
    price: float
