import os
import psycopg

DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")


def get_connection():
    return psycopg.connect(
        dbname='fastapi',
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD)

def show_cart(): # Opening with 'with' ensures connection and cursor is closed
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart")
            return cur.fetchall()
