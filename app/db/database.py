import os, time
import psycopg
from app.config import settings
from psycopg_pool import ConnectionPool

pool = ConnectionPool(
    conninfo=(
        f"dbname=fastapi user={settings.postgres_user} password={settings.postgres_password} host={settings.postgres_host}"
    )
)

def get_connection():
    return pool.connection()


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
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("INSERT INTO cart(item_name, quantity) values(%s, %s)", (item.item_name, item.quantity))

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
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("UPDATE cart SET quantity=%s WHERE id=%s RETURNING *", (quantity,item_id))
            return cur.fetchone()

def create_user(user):
    with pool.connection() as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute("INSERT INTO users(email,password) values(%s,%s) RETURNING *", (user.email, user.password))
            return cur.fetchone()