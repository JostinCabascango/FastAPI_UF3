from fastapi import APIRouter
from database import get_connection

router = APIRouter()


def fetch_categories(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM public.category")
        return cursor.fetchall()


@router.get("/category/")
async def get_categories():
    connection = get_connection()
    categories = fetch_categories(connection)
    return categories
