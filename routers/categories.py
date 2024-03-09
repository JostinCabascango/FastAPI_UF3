from fastapi import APIRouter, HTTPException
from models import Category
from services import category_service

router = APIRouter()


@router.get("/category/")
async def get_categories():
    """Fetch all categories from the database."""
    categories = category_service.fetch_categories()
    if not categories:
        return {"message": "No categories found"}
    return categories


@router.get("/category/{category_id}")
async def get_category(category_id: int):
    """Fetch a category by its ID."""
    category = category_service.fetch_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    return category


@router.post("/category/")
async def post_category(category: Category):
    """Create a new category in the database."""
    return category_service.create_category(category)


@router.put("/category/{category_id}")
async def put_category(category_id: int, category: Category):
    """Update a category in the database."""
    update_result = category_service.update_category(category_id, category)
    message = update_result["message"]

    if "does not exist" in message:
        raise HTTPException(status_code=404, detail=message)
    elif "No changes were made" in message:
        raise HTTPException(status_code=400, detail=message)
    elif "Failed" in message:
        raise HTTPException(status_code=500, detail=message)

    return update_result


@router.delete("/category/{id}")
async def delete_category(id: int):
    """Delete a category from the database."""
    return category_service.delete_category(id)
