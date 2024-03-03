from fastapi import APIRouter, HTTPException
from database import get_connection
from models import Subcategory
from services import subcategory_service

router = APIRouter()


@router.get("/subcategories/")
async def get_subcategories():
    return subcategory_service.fetch_subcategories()


@router.get("/subcategory/{subcategory_id}")
async def get_subcategory(subcategory_id: int):
    subcategory = subcategory_service.fetch_subcategory(subcategory_id)
    if subcategory is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory


@router.post("/subcategory/")
async def post_subcategory(subcategory: Subcategory):
    if not subcategory_service.create_subcategory(subcategory):
        raise HTTPException(status_code=400, detail="Failed to create subcategory")
    return {"message": "Subcategory created successfully"}


@router.put("/subcategory/{id}")
async def put_subcategory(id: int, subcategory: Subcategory):
    if not subcategory_service.update_subcategory(id, subcategory):
        raise HTTPException(status_code=400, detail="Failed to update subcategory")
    return {"message": "Subcategory updated successfully"}


@router.delete("/subcategory/{id}")
async def delete_subcategory(id: int):
    if not subcategory_service.delete_subcategory(id):
        raise HTTPException(status_code=400, detail="Failed to delete subcategory")
    return {"message": "Subcategory deleted successfully"}
