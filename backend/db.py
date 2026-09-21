import mysql.connector
import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "noreste_grill")
    )


@contextmanager
def get_cursor(dictionary=True):
    """Entrega (conn, cursor) para la Data Access Layer y cierra ambos al salir."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield conn, cursor
    finally:
        cursor.close()
        conn.close()
