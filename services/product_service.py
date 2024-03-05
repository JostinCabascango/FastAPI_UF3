from datetime import datetime
from typing import List
import csv

from database import get_connection
from models import ProductInDB, ProductUpdate, ProductSubcategoryCategory, Category, Subcategory, ProductCreateCSV
from services import category_service, subcategory_service


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


def fetch_products_orderby(orderby):
    if orderby not in ["asc", "desc"]:
        raise ValueError("Valor inválido para ordenar. Se esperaba 'asc' o 'desc'.")

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
    return ProductSubcategoryCategory(
        category_name=data[0],
        subcategory_name=data[1],
        product_name=data[2],
        product_brand=data[3],
        price=data[4]
    )


async def create_or_update_product(product):
    if not product_exists(product.product_id):
        create_product(product)
    else:
        update_product(product.product_id, product)


async def load_products(file):
    try:
        contents = await file.read()
        reader = csv.reader(contents.decode("utf-8").splitlines(), delimiter=",")
        next(reader)
        for row in reader:
            category = Category(
                category_id=row[0],
                name=row[1],
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            subcategory = Subcategory(
                subcategory_id=int(row[2]),
                name=row[3],
                category_id=int(row[0]),
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            product = ProductCreateCSV(
                product_id=int(row[4]),
                name=row[5],
                description=row[6],
                company=row[7],
                price=float(row[8]),
                units=int(row[9]),
                subcategory_id=int(row[2])
            )
            category_service.create_or_update_category(category)
            subcategory_service.create_or_update_subcategory(subcategory)
            create_or_update_product(product)
    except Exception as e:
        return {"message": "Error loading products", "success": False}

    return {"message": "Products loaded successfully", "success": True}
