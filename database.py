from psycopg import connect

DATABASE_CONNECTION_STRING = "postgresql://user_postgres:pass_postgres@localhost:5432/Ecommerce"


def get_connection():
    try:
        return connect(DATABASE_CONNECTION_STRING)
    except Exception as e:
        raise e
