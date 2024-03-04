from database import get_connection


def fetch_categories():
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.category")
        return cursor.fetchall()


def fetch_category(category_id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.category WHERE category_id = %s", (category_id,))
        return cursor.fetchone()


def create_category(category):
    with get_connection().cursor() as cursor:
        cursor.execute("INSERT INTO public.category (category_id, name) VALUES (%s, %s)",
                       (category.category_id, category.name))
    get_connection().commit()
    return cursor.rowcount > 0


def update_category(category_id, category):
    with get_connection().cursor() as cursor:
        cursor.execute("UPDATE public.category SET name = %s WHERE category_id = %s", (category.name, category_id))
    get_connection().commit()
    return cursor.rowcount > 0


def delete_category(category_id):
    with get_connection().cursor() as cursor:
        cursor.execute("DELETE FROM public.category WHERE category_id = %s", (category_id,))
    get_connection().commit()
    return cursor.rowcount > 0


def category_exists(category_id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.category WHERE category_id = %s", (category_id,))
        return bool(cursor.fetchone())
