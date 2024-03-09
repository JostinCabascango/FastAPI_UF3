from typing import Dict

from fastapi import HTTPException
from psycopg import Error

from utils.apiResponse import ApiResponse
from database import get_connection
from models import Subcategory


def execute_query(query: str, params: tuple = None):
    """Execute a query and return the results."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                results = cursor.fetchall()
            else:
                results = cursor.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if conn is not None and not conn.closed:
            conn.close()
    return results


def fetch_subcategories():
    """Fetch all subcategories from the database."""
    return execute_query("SELECT * FROM public.subcategory")


def fetch_subcategory(subcategory_id: int):
    """Fetch a subcategory by its ID."""
    query = "SELECT * FROM public.subcategory WHERE subcategory_id = %s"
    return execute_query(query, (subcategory_id,))


def execute_insert_query(query: str, params: tuple) -> int:
    """Execute an insert query and return the number of affected rows."""
    try:
        return execute_query(query, params)
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_subcategory(subcategory: Subcategory):
    """Create a new subcategory in the database."""
    query = "INSERT INTO public.subcategory (name, category_id,created_at,updated_at) VALUES (%s, %s, NOW(), NOW())"
    rows_affected = execute_insert_query(query, (subcategory.name, subcategory.category_id))
    if rows_affected == 0:
        response = ApiResponse("failed", "No changes were made", True)
    else:
        response = ApiResponse("success", "Subcategory created successfully", False)

    return response.convert_to_dict()


def execute_update_query(query: str, params: tuple) -> int:
    """Execute an update query and return the number of affected rows."""
    try:
        return execute_query(query, params)
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))


def update_subcategory(subcategory_id: int, subcategory: Subcategory):
    """Update an existing subcategory in the database."""
    query = "UPDATE public.subcategory SET name = %s,updated_at = NOW() WHERE subcategory_id = %s"
    rows_affected = execute_update_query(query, (subcategory.name, subcategory_id))
    if rows_affected == 0:
        response = ApiResponse("failed", "No changes were made", True)
    else:
        response = ApiResponse("success", "Subcategory updated successfully", False)
    return response.convert_to_dict()


def delete_subcategory(subcategory_id: int) -> Dict[str, str]:
    """Delete a subcategory from the database."""
    query = "DELETE FROM public.subcategory WHERE subcategory_id = %s"
    rows_affected = execute_delete_query(query, (subcategory_id,))

    if rows_affected == 0:
        response = ApiResponse("failed", "No changes were made", True)
    else:
        response = ApiResponse("success", "Subcategory deleted successfully", False)
    return response.convert_to_dict()


def execute_delete_query(query: str, params: tuple) -> int:
    """Execute a delete query and return the number of affected rows."""
    try:
        return execute_query(query, params)
    except Error as e:
        raise HTTPException(status_code=400, detail=str(e))


def subcategory_exists(subcategory_id: int):
    """Check if a subcategory exists in the database."""
    query = "SELECT * FROM public.subcategory WHERE subcategory_id = %s"
    return True if execute_query(query, (subcategory_id,)) else False
