from app.db import database

def show_prod(limit):
    return database.get_products(limit)