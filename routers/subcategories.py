from fastapi import APIRouter, HTTPException
from models import Subcategory
from services import subcategory_service

router = APIRouter()

"""GET routes"""


@router.get("/subcategories/", summary="Get all subcategories")
async def get_all_subcategories():
    """Fetch all subcategories from the database."""
    subcategories = subcategory_service.fetch_subcategories()
    if not subcategories:
        raise HTTPException(status_code=404, detail="No subcategories found")
    return subcategories


@router.get("/subcategory/{subcategory_id}", summary="Get a subcategory by ID")
async def get_subcategory_by_id(subcategory_id: int):
    """Fetch a subcategory by its ID from the database."""
    subcategory = subcategory_service.fetch_subcategory(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail=f"Subcategory {subcategory_id} not found")
    return subcategory


"""POST routes"""


@router.post("/subcategory/", summary="Create a new subcategory")
async def create_subcategory(subcategory: Subcategory):
    """Create a new subcategory in the database."""
    created_subcategory = subcategory_service.create_subcategory(subcategory)
    if not created_subcategory:
        raise HTTPException(status_code=400, detail="Failed to create subcategory")
    return {"message": "Subcategory created successfully"}


"""PUT routes"""


@router.put("/subcategory/{subcategory_id}", summary="Update a subcategory")
async def update_subcategory(subcategory_id: int, subcategory: Subcategory):
    """Update a subcategory in the database."""
    updated_subcategory = subcategory_service.update_subcategory(subcategory_id, subcategory)
    if not updated_subcategory:
        raise HTTPException(status_code=500, detail="Failed to update subcategory.")
    return updated_subcategory


"""DELETE routes"""


@router.delete("/subcategory/{subcategory_id}", summary="Delete a subcategory")
async def delete_subcategory(subcategory_id: int):
    """Delete a subcategory from the database."""
    deletion_success = subcategory_service.delete_subcategory(subcategory_id)
    if not deletion_success:
        raise HTTPException(status_code=500, detail="Failed to delete subcategory.")
    return {"message": "Subcategory deleted successfully"}
