from fastapi import APIRouter, HTTPException
from database import get_connection
from models import Category
from services import category_service

router = APIRouter()


@router.get("/category/")
async def get_categories():
    return category_service.fetch_categories()


@router.get("/category/{category_id}")
async def get_category(category: int):
    category = category_service.fetch_category(category)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/category/")
async def post_category(category: Category):
    if not category_service.create_category(category):
        raise HTTPException(status_code=400, detail="Failed to create category")
    return {"message": "Category created successfully"}


@router.put("/category/{id}")
async def put_category(id: int, category: Category):
    if not category_service.update_category(id, category):
        raise HTTPException(status_code=400, detail="Failed to update category")
    return {"message": "Category updated successfully"}


@router.delete("/category/{id}")
async def delete_category(id: int):
    if not category_service.delete_category(id):
        raise HTTPException(status_code=400, detail="Failed to delete category")
    return {"message": "Category deleted successfully"}
