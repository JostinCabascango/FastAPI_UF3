from typing import List
import csv
from fastapi import APIRouter, HTTPException, UploadFile, File
from models import ProductCreate, ProductUpdate, ProductInDB, Category, Subcategory, ProductCreateCSV
from services import product_service, category_service, subcategory_service

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
    result = product_service.create_product(product)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"message": "Added successfully"}


@router.put("/product/{id}")
async def put_product(id: int, product: ProductUpdate):
    product_service.update_product(id, product)
    return {"message": "Successfully modified"}


@router.delete("/product/{id}")
async def delete_product(id: int):
    result = product_service.delete_product(id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": "Deleted successfully"}


@router.post("/loadProducts/")
async def load_products(file: UploadFile = File(...)):
    try:
        content = await file.read()
        reader = csv.reader(content.decode('utf-8').splitlines(), delimiter=',')
        next(reader)
        for row in reader:
            category = Category(
                category_id=int(row[0]),
                name=row[1]
            )
            subcategory = Subcategory(
                subcategory_id=int(row[2]),
                name=row[3],
                category_id=int(row[0])
            )
            product = ProductCreateCSV(
                product_id=int(row[4]),
                name=row[5],
                description=row[6],
                company=row[7],
                price=float(row[8]),
                units=int(row[9]),
                subcategory_id=int(row[2])
            )
            if not category_service.category_exists(category.category_id):
                category_service.create_category(category)
            else:
                category_service.update_category(category.category_id, category)

            if not subcategory_service.subcategory_exists(subcategory.subcategory_id):
                subcategory_service.create_subcategory(subcategory)
            else:
                subcategory_service.update_subcategory(subcategory.subcategory_id, subcategory)

            if not product_service.product_exists(product.product_id):
                product_service.create_product(product)
            else:
                product_service.update_product(product.product_id, product)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file: {str(e)}")

    return {"message": "Data loaded successfully"}
