from datetime import datetime
from typing import List
from fastapi import HTTPException
from database import get_connection
from models import ProductInDB, ProductUpdate, ProductSubcategoryCategory


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


def create_product_from_data(data: tuple) -> ProductInDB:
    """Create a ProductInDB object from a tuple of data."""
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
    """Fetch all products from the database."""
    query = "SELECT * FROM public.product"
    data = execute_query(query)
    return [create_product_from_data(product_data) for product_data in data]


def fetch_product(id: int) -> ProductInDB:
    """Fetch a product by its ID."""
    query = "SELECT * FROM public.product WHERE product_id = %s"
    data = execute_query(query, (id,))
    return create_product_from_data(data[0]) if data else None


def create_product(product: ProductInDB):
    """Create a new product in the database."""
    if not subcategory_exists(product.subcategory_id):
        raise Exception("Subcategory not found")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created_at = product.created_at if product.created_at else current_time
    updated_at = product.updated_at if product.updated_at else current_time
    query = "INSERT INTO public.product (name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    execute_query(query, (
        product.name, product.description, product.company, product.price, product.units, product.subcategory_id,
        created_at, updated_at))


def product_exists(id: int) -> bool:
    """Check if a product exists in the database."""
    query = "SELECT * FROM public.product WHERE product_id = %s"
    data = execute_query(query, (id,))
    return bool(data)


def subcategory_exists(id: int) -> bool:
    """Check if a subcategory exists in the database."""
    query = "SELECT * FROM public.subcategory WHERE subcategory_id = %s"
    data = execute_query(query, (id,))
    return bool(data)


def update_product(id: int, product: ProductUpdate):
    """Update an existing product in the database."""
    try:
        if not product_exists(id) or not subcategory_exists(product.subcategory_id):
            raise Exception("Product or subcategory not found")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = "UPDATE public.product SET name = %s, description = %s, company = %s, price = %s, units = %s, subcategory_id = %s, updated_at = %s WHERE product_id = %s"
        rows_affected = execute_query(query, (
            product.name, product.description, product.company, product.price, product.units, product.subcategory_id,
            current_time, id))

        if rows_affected == 0:
            raise Exception("Update operation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_product(id: int):
    """Delete a product from the database."""
    if not product_exists(id):
        raise Exception("Product not found")
    query = "DELETE FROM public.product WHERE product_id = %s"
    execute_query(query, (id,))


def fetch_products_orderby(orderby):
    """Fetch all products from the database ordered by name."""
    if orderby not in ["asc", "desc"]:
        raise ValueError("Invalid value for ordering. Expected 'asc' or 'desc'.")

    query = f"""
    SELECT category.name, subcategory.name, product.name, product.company, product.price
    FROM public.product
    INNER JOIN public.subcategory ON product.subcategory_id = subcategory.subcategory_id
    INNER JOIN public.category ON subcategory.category_id = category.category_id
    ORDER BY product.name {orderby}
    """
    data = execute_query(query)
    return [create_product_with_subcategory_from_data(product_data) for product_data in data]


def fetch_products_contain(name):
    """Fetch all products from the database that contain a given name."""
    query = f"""
    SELECT category.name, subcategory.name, product.name, product.company, product.price
    FROM public.product
    INNER JOIN public.subcategory ON product.subcategory_id = subcategory.subcategory_id
    INNER JOIN public.category ON subcategory.category_id = category.category_id
    WHERE product.name LIKE %s
    """
    data = execute_query(query, (f"%{name}%",))
    return [create_product_with_subcategory_from_data(product_data) for product_data in data]


def fetch_products_skip_limit(skip, limit):
    """Fetch a limited number of products from the database with an offset."""
    query = f"""
    SELECT category.name, subcategory.name, product.name, product.company, product.price
    FROM public.product
    INNER JOIN public.subcategory ON product.subcategory_id = subcategory.subcategory_id
    INNER JOIN public.category ON subcategory.category_id = category.category_id
    Limit %s Offset %s
    """
    data = execute_query(query, (limit, skip))
    return [create_product_with_subcategory_from_data(product_data) for product_data in data]


def create_product_with_subcategory_from_data(data: tuple) -> ProductSubcategoryCategory:
    """Create a ProductSubcategoryCategory object from a tuple of data."""
    return ProductSubcategoryCategory(
        category_name=data[0],
        subcategory_name=data[1],
        product_name=data[2],
        product_brand=data[3],
        price=data[4]
    )
