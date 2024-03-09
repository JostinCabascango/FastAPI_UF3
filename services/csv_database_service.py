from fastapi import UploadFile
from database import get_connection
import csv
from models import Category, ProductCreateCSV, Subcategory


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


def create_or_update_category(category: Category):
    """Create or update a category in the database."""
    query = "INSERT INTO public.category (category_id, name, created_at, updated_at) VALUES (%s, %s, NOW(), NOW()) ON CONFLICT (category_id) DO UPDATE SET name = %s, updated_at = NOW()"
    params = (category.category_id, category.name, category.name)
    execute_query(query, params)


def create_or_update_subcategory(subcategory: Subcategory):
    """Create or update a subcategory in the database."""
    query = "INSERT INTO public.subcategory (subcategory_id, name, category_id, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW()) ON CONFLICT (subcategory_id) DO UPDATE SET name = %s, category_id = %s, updated_at = NOW()"
    params = (subcategory.subcategory_id, subcategory.name, subcategory.category_id, subcategory.name,
              subcategory.category_id)
    execute_query(query, params)


def create_or_update_product(product: ProductCreateCSV):
    """Create or update a product in the database."""
    query = "INSERT INTO public.product (product_id, name, description, company, price, units, subcategory_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW()) ON CONFLICT (product_id) DO UPDATE SET name = %s, description = %s, company = %s, price = %s, units = %s, subcategory_id = %s, updated_at = NOW()"
    params = (product.product_id, product.name, product.description, product.company, product.price, product.units,
              product.subcategory_id, product.name, product.description, product.company, product.price,
              product.units, product.subcategory_id)
    execute_query(query, params)


async def load_data_from_csv(file: UploadFile):
    """Load data from a CSV file into the database."""
    try:
        contents = await file.read()
        reader = csv.reader(contents.decode('utf-8').splitlines(), delimiter=',')
        next(reader)
        for row in reader:
            try:
                category = Category(
                    category_id=int(row[0]),
                    name=row[1]
                )
                create_or_update_category(category)
            except Exception as e:
                raise Exception(f"Error creating or updating category: {e}")

            try:
                subcategory = Subcategory(
                    subcategory_id=int(row[2]),
                    name=row[3],
                    category_id=int(row[0])
                )
                create_or_update_subcategory(subcategory)
            except Exception as e:
                raise Exception(f"Error creating or updating subcategory: {e}")

            try:
                product = ProductCreateCSV(
                    product_id=int(row[4]),
                    name=row[5],
                    description=row[6],
                    company=row[7],
                    price=float(row[8]),
                    units=int(row[9]),
                    subcategory_id=int(row[2])
                )
                create_or_update_product(product)
            except Exception as e:
                raise Exception(f"Error creating or updating product: {e}")
    except Exception as e:
        raise Exception("Error loading data from CSV", e)
