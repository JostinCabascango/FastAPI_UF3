from typing import List
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from models import ProductCreate, ProductUpdate, ProductInDB
from services import product_service, csv_database_service
from utils.apiResponse import ApiResponse

router = APIRouter()

"""GET /products/"""


@router.get("/products/", response_model=List[ProductInDB], summary="Get all products")
async def get_products():
    """Fetch all products from the database."""
    try:
        products = product_service.fetch_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/product/{id}", response_model=ProductInDB, summary="Get a product by ID")
async def get_product(id: int):
    """Fetch a single product by its ID from the database."""
    product = product_service.fetch_product(id)
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    return product


@router.get("/products/orderby/", summary="Get products ordered by price")
async def get_products_orderby(orderby: str = Query(None, enum=["asc", "desc"])):
    """Fetch all products ordered by price from the database."""
    try:
        return product_service.fetch_products_orderby(orderby)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/products/contain/", summary="Get products that contain a string")
async def get_products_contain(name: str):
    """Fetch all products that contain a given string in their name from the database."""
    try:
        return product_service.fetch_products_contain(name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/skip_limit/", summary="Get a range of products")
async def get_products_skip_limit(skip: int, limit: int):
    """Fetch a range of products with skip and limit from the database."""
    try:
        return product_service.fetch_products_skip_limit(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""POST /products/"""


@router.post("/product/", summary="Create a new product")
async def post_product(product: ProductCreate):
    """Create a new product in the database."""
    try:
        product_service.create_product(product)
        return ApiResponse(status=200, message="Product created successfully", data=product).convert_to_dict()
    except Exception as e:
        return ApiResponse(status=400, message=str(e), data=False).convert_to_dict()


@router.post("/loadProducts/", summary="Upload a CSV file")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file and load its data into the database."""
    try:
        await csv_database_service.load_data_from_csv(file)
        return {"message": "File uploaded successfully and data loaded into the database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


"""PUT /products/"""


@router.put("/product/{id}", summary="Update a product")
async def put_product(id: int, product: ProductUpdate):
    """Update an existing product in the database."""
    try:
        product_service.update_product(id, product)
        return ApiResponse(status=200, message="Product updated successfully", data=product).convert_to_dict()
    except Exception as e:
        return ApiResponse(status=400, message=str(e), data=False).convert_to_dict()


"""DELETE /products/"""


@router.delete("/product/{id}", summary="Delete a product")
async def delete_product(id: int):
    """Delete a product by its ID from the database."""
    try:
        product_service.delete_product(id)
        return ApiResponse(status=200, message="Product deleted successfully", data=True).convert_to_dict()
    except Exception as e:
        return ApiResponse(status=400, message=str(e), data=False).convert_to_dict()
