from fastapi import APIRouter, HTTPException
from models import Category
from services import category_service

router = APIRouter()

"""GET /categories/"""


@router.get("/categories/")
async def get_all_categories():
    """Fetch all categories from the database."""
    categories = category_service.fetch_categories()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return categories


@router.get("/category/{category_id}", summary="Get a category by ID")
async def get_category_by_id(category_id: int):
    """Fetch a category by its ID from the database."""
    category = category_service.fetch_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail=f"Category {category_id} not found")
    return category


"""POST /category/"""


@router.post("/category/", summary="Create a new category")
async def post_category(category: Category):
    """Create a new category in the database."""
    return category_service.create_category(category)


"""PUT /category/"""


@router.put("/category/{category_id}", summary="Update a category")
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


"""DELETE /category/"""


@router.delete("/category/{category_id}", summary="Delete a category")
async def delete_category(category_id: int):
    """Delete a category from the database."""
    return category_service.delete_category(category_id)
