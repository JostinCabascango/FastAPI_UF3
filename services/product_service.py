from datetime import datetime
from typing import List

from database import get_connection
from models import ProductInDB, ProductUpdate


def execute_query(query: str, params: tuple = None):
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
        conn.close()
    return results


def create_product_from_data(data: tuple) -> ProductInDB:
    return ProductInDB(
        product_id=data[0],
        name=data[1],
        description=data[2],
        company=data[3],
        price=data[4],
        units=data[5],
        subcategory_id=data[6],
        created_at=data[7].strftime("%Y-%m-%d %H:%M:%S"),
        updated_at=data[8].strftime("%Y-%m-%d %H:%M:%S")
    )


def fetch_products() -> List[ProductInDB]:
    query = "SELECT * FROM public.product"
    data = execute_query(query)
    return [create_product_from_data(product_data) for product_data in data]


def fetch_product(id: int) -> ProductInDB:
    query = "SELECT * FROM public.product WHERE product_id = %s"
    data = execute_query(query, (id,))
    return create_product_from_data(data[0]) if data else None


def create_product(product: ProductInDB):
    if not subcategory_exists(product.subcategory_id):
        return {"message": "Subcategory not found", "success": False}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = "INSERT INTO public.product (name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    execute_query(query, (
        product.name, product.description, product.company, product.price, product.units, product.subcategory_id,
        current_time, current_time))

    return {"message": "Added successfully", "success": True}


def product_exists(id: int) -> bool:
    query = "SELECT * FROM public.product WHERE product_id = %s"
    data = execute_query(query, (id,))
    return bool(data)


def subcategory_exists(id: int) -> bool:
    query = "SELECT * FROM public.subcategory WHERE subcategory_id = %s"
    data = execute_query(query, (id,))
    return bool(data)


def update_product(id: int, product: ProductUpdate):
    if not product_exists(id) or not subcategory_exists(product.subcategory_id):
        return {"message": "Product or subcategory not found"}
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query = "UPDATE public.product SET name = %s, description = %s, company = %s, price = %s, units = %s, subcategory_id = %s, updated_at = %s WHERE product_id = %s"
    rows_affected = execute_query(query, (
        product.name, product.description, product.company, product.price, product.units, product.subcategory_id,
        current_time, id))

    if rows_affected > 0:
        return {"message": "Successfully modified"}
    else:
        return {"message": "Update operation failed"}


def delete_product(id: int):
    if not product_exists(id):
        return {"message": "Product not found", "success": False}
    query = "DELETE FROM public.product WHERE product_id = %s"
    execute_query(query, (id,))
    return {"message": "Deleted successfully", "success": True}
