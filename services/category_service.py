from psycopg import Error, DatabaseError, sql

from database import get_connection
from models import Category

FETCH_CATEGORIES_SQL = sql.SQL("SELECT * FROM public.category")
FETCH_CATEGORY_SQL = sql.SQL("SELECT * FROM public.category WHERE category_id = %s")
INSERT_CATEGORY_SQL = sql.SQL("""
    INSERT INTO public.category (category_id, name, created_at, updated_at) 
    VALUES (%s, %s, NOW(), NOW())
""")
UPDATE_CATEGORY_SQL = sql.SQL("""
    UPDATE public.category SET name = %s, updated_at = NOW() WHERE category_id = %s
""")
DELETE_CATEGORY_SQL = sql.SQL("DELETE FROM public.category WHERE category_id = %s")


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


def fetch_categories():
    """Fetch all categories from the database."""
    return execute_query(FETCH_CATEGORIES_SQL)


def fetch_category(category_id: int):
    """Fetch a category by its ID."""
    return execute_query(FETCH_CATEGORY_SQL, (category_id,))


def create_category(category: Category):
    """Create a new category in the database."""
    try:
        execute_query(INSERT_CATEGORY_SQL, (category.category_id, category.name))
        return {"message": "Category created successfully"}
    except DatabaseError as e:
        return {"message": f"Failed to create category: {str(e)}"}
    except Error as e:
        return {"message": f"Unexpected error occurred: {str(e)}"}


def update_category(category_id: int, category: Category):
    """Update an existing category in the database."""
    if not category_exists(category_id):
        return {"message": f"Category with id {category_id} does not exist"}

    rows_affected = execute_query(UPDATE_CATEGORY_SQL, (category.name, category_id))
    if rows_affected > 0:
        return {"message": "Category updated successfully"}
    else:
        return {"message": "No changes were made"}


def delete_category(category_id: int):
    """Delete a category from the database."""
    if not category_exists(category_id):
        return {"message": f"Category with id {category_id} does not exist"}

    try:
        execute_query(DELETE_CATEGORY_SQL, (category_id,))
        return {"message": "Category deleted successfully"}
    except Error as e:
        return {"message": f"Failed to delete category with id {category_id}: {str(e)}"}


def category_exists(category_id: int):
    """Check if a category exists in the database."""
    return bool(fetch_category(category_id))


async def create_or_update_category(category: Category):
    if not category_exists(category.category_id):
        create_category(category)
    else:
        update_category(category.category_id, category)
