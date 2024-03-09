from fastapi import APIRouter, HTTPException
from database import get_connection
from models import Subcategory
from services import subcategory_service

router = APIRouter()


@router.get("/subcategories/")
async def get_subcategories():
    subcategories = subcategory_service.fetch_subcategories()
    if not subcategories:
        return {"message": "No subcategories found"}
    return subcategories


@router.get("/subcategory/{subcategory_id}")
async def get_subcategory(subcategory_id: int):
    subcategory = subcategory_service.fetch_subcategory(subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail=f"Subcategory {subcategory_id} not found")
    return subcategory


@router.post("/subcategory/")
async def post_subcategory(subcategory: Subcategory):
    if not subcategory_service.create_subcategory(subcategory):
        raise HTTPException(status_code=400, detail="Failed to create subcategory")
    return {"message": "Subcategory created successfully"}


@router.put("/subcategory/{subcategory_id}")
async def put_subcategory(subcategory_id: int, subcategory: Subcategory):
    try:
        return subcategory_service.update_subcategory(subcategory_id, subcategory)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.delete("/subcategory/{subcategory_id}")
async def delete_subcategory(subcategory_id: int):
    """Delete a subcategory from the database."""
    try:
        return subcategory_service.delete_subcategory(subcategory_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
