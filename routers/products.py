from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from models import ProductCreate, ProductUpdate, ProductInDB
from services import product_service, csv_database_service

router = APIRouter()


@router.get("/products/", response_model=List[ProductInDB])
async def get_products():
    return product_service.fetch_products()


@router.get("/product/{id}", response_model=ProductInDB)
async def get_product(id: int):
    product = product_service.fetch_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    return product


@router.post("/product/")
async def post_product(product: ProductCreate):
    result = product_service.create_product(product)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": "Added successfully"}


@router.put("/product/{id}")
async def put_product(id: int, product: ProductUpdate):
    try:
        product_service.update_product(id, product)
        return {"message": "Successfully modified"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/product/{id}")
async def delete_product(id: int):
    result = product_service.delete_product(id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": "Deleted successfully"}


@router.post("/loadProducts/")
async def upload_csv(file: UploadFile = File(...)):
    try:
        await csv_database_service.load_data_from_csv(file)
        return {"message": "File uploaded successfully and data loaded into the database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/orderby/")
async def get_products_orderby(orderby: str = Query(None, enum=["asc", "desc"])):
    return product_service.fetch_products_orderby(orderby)


@router.get("/products/contain/")
async def get_products_contain(name: str):
    return product_service.fetch_products_contain(name)


@router.get("/products/skip_limit/")
async def get_products_skip_limit(skip: int, limit: int):
    return product_service.fetch_products_skip_limit(skip, limit)
