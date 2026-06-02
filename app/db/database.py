import os
import psycopg
from app.schema.schema import AddToCart

DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")


def get_connection():
    return psycopg.connect(
        dbname='fastapi',
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD)

def get_item_by_name(item_name: str):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart WHERE item_name=%s", (item_name,))
            return cur.fetchone()

def get_item_by_id(item_id: int):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart WHERE id=%s", (item_id,))
            return cur.fetchone()

def get_cart(): # Opening with 'with' ensures connection and cursor is closed
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart")
            return cur.fetchall()

def add_to_cart(item):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("INSERT INTO cart(item_name, quantity) values(%s, %s)", (item.item_name, item.quantity))

def delete_from_cart(item_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cart WHERE item_name=%s",(item_name,))

def clear_cart():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cart")

def update_quantity(id,quantity):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("UPDATE cart SET quantity=%s WHERE id=%s", (quantity,id))