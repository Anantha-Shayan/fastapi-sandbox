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

def get_cart(): # Opening with 'with' ensures connection and cursor is closed
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart")
            return cur.fetchall()

def get_cart_item(id):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(f"SELECT * FROM cart WHERE id={id}")
            return cur.fetchone()

def add_to_cart(item):
    with get_connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(f"INSERT INTO cart(item_name, quantity) values('{item.item_name}', {item.quantity})")

def delete_from_cart(item_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"DELETE FROM cart WHERE item_name='{item_name}'")

def clear_cart():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cart")
