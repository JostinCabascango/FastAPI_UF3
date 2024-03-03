from psycopg import connect

DATABASE_CONNECTION_STRING = "postgresql://user_postgres:pass_postgres@localhost:5432/Ecommerce"


def get_connection():
    """
    ESTABLE Y DEVUELVE UNA CONEXIÓN A LA BASE DE DATOS
    """
    return connect(DATABASE_CONNECTION_STRING)
