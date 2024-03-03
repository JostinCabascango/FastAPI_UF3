from fastapi import APIRouter
from database import get_connection

router = APIRouter()


def fetch_subcategories(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.subcategory")
        return cursor.fetchall()


@router.get("/subcategory/")
async def get_subcategories():
    connection = get_connection()
    subcategories = fetch_subcategories(connection)
    return subcategories
