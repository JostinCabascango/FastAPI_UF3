from database import get_connection


def fetch_subcategories():
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.subcategory")
        return cursor.fetchall()


def fetch_subcategory(subcategory_id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.subcategory WHERE subcategory_id = %s", (subcategory_id,))
        return cursor.fetchone()


def create_subcategory(subcategory):
    with get_connection().cursor() as cursor:
        cursor.execute("INSERT INTO public.subcategory (subcategory_id, name, category_id) VALUES (%s, %s, %s)",
                       (subcategory.subcategory_id, subcategory.name, subcategory.category_id))
    get_connection().commit()
    return cursor.rowcount > 0


def update_subcategory(subcategory_id, subcategory):
    with get_connection().cursor() as cursor:
        cursor.execute("UPDATE public.subcategory SET name = %s, category_id = %s WHERE subcategory_id = %s",
                       (subcategory.name, subcategory.category_id, subcategory_id))
    get_connection().commit()
    return cursor.rowcount > 0


def delete_subcategory(subcategory_id):
    with get_connection().cursor() as cursor:
        cursor.execute("DELETE FROM public.subcategory WHERE subcategory_id = %s", (subcategory_id,))
    get_connection().commit()
    return cursor.rowcount > 0


def subcategory_exists(subcategory_id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM public.subcategory WHERE subcategory_id = %s", (subcategory_id,))
        return bool(cursor.fetchone())


async def create_or_update_subcategory(subcategory):
    if not subcategory_exists(subcategory.subcategory_id):
        create_subcategory(subcategory)
    else:
        update_subcategory(subcategory.subcategory_id, subcategory)
