import os, time
import psycopg
from app.schema.schema import AddToCart
from app.config import settings
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo=(
        f"dbname=fastapi user={settings.postgres_user} password={settings.postgres_password} host={settings.postgres_host}"
    )
)

def get_connection():
    return psycopg.connect(
        dbname='fastapi',
        host=settings.postgres_host,
        user=settings.postgres_user,
        password=settings.postgres_password)

def get_item_by_name(item_name: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart WHERE item_name=%s", (item_name,))
            # Using %s in query and then passing the data in tuple - (item_name,)
            # will prevent SQL INJECTION
            # Hence, Never build SQL with f-strings 
            return cur.fetchone()

def get_item_by_id(item_id: int):
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart WHERE id=%s", (item_id,))
            return cur.fetchone()

def get_cart(): # Opening with 'with' ensures connection and cursor is closed
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("SELECT * FROM cart")
            return cur.fetchall()

def add_to_cart(item):
    start = time.perf_counter()
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("INSERT INTO cart(item_name, quantity) values(%s, %s)", (item.item_name, item.quantity))
    print(f"DB add to cart: {str((time.perf_counter() - start)*1000)}ms")

def delete_from_cart(item_name):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cart WHERE item_name=%s RETURNING *",(item_name,))
            return cur.fetchone()

def clear_cart():
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cart")

def update_quantity(item_id,quantity):
    start = time.perf_counter()
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("UPDATE cart SET quantity=%s WHERE id=%s RETURNING *", (quantity,item_id))
            print(f"DB update cart: {str((time.perf_counter() - start)*1000)}ms")
            return cur.fetchone()