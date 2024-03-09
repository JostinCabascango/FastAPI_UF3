from fastapi import FastAPI

from routers import products, categories, subcategories

app = FastAPI(
    title="Product Management API with FastAPI and PostgreSQL",
    description="""
    This is a FastAPI application that provides CRUD operations for managing products, categories, and subcategories. 
    It uses PostgreSQL as the database to store the data. 
    The API provides endpoints for creating, retrieving, updating, and deleting products, categories, and subcategories.
    """,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json"
)

app.include_router(products.router, prefix="/products", tags=["Products"],
                   responses={404: {"description": "Not found"}})
app.include_router(categories.router, prefix="/categories", tags=["Categories"],
                   responses={404: {"description": "Not found"}})
app.include_router(subcategories.router, prefix="/subcategories", tags=["Subcategories"],
                   responses={404: {"description": "Not found"}})
