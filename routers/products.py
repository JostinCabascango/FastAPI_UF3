from typing import List

from fastapi import APIRouter, HTTPException
from models import ProductCreate, ProductUpdate, ProductInDB
from services import product_service

router = APIRouter()


@router.get("/products/", response_model=List[ProductInDB])
async def get_products():
    return product_service.fetch_products()


@router.get("/product/{id}", response_model=ProductInDB)
async def get_product(id: int):
    product = product_service.fetch_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/product/")
async def post_product(product: ProductCreate):
    product_service.create_product(product)
    return {"message": "Added successfully"}


@router.put("/product/{id}")
async def put_product(id: int, product: ProductUpdate):
    product_service.update_product(id, product)
    return {"message": "Successfully modified"}


@router.delete("/product/{id}")
async def delete_product(id: int):
    product_service.delete_product(id)
    return {"message": "Deleted successfully"}
