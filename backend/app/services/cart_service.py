import psycopg
from app.db import database
from app.exceptions import exceptions

def add_item(item):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	try:
		database.insert_item_to_cart(item)
	except psycopg.errors.UniqueViolation:
		raise exceptions.ItemAlreadyExists()
	return {"message": f"{item.item_name} added to cart"}

def update_item(item_id, quantity):
	updated_item = database.update_quantity(item_id, quantity)
	if not updated_item:
		raise exceptions.ItemDoesNotExist()
	return {
		'message': "Item Quantity updated",
		'data' : updated_item
		}

def delete_item(item_name):
    deleted_item = database.delete_from_cart(item_name)
    if not deleted_item:
        raise exceptions.ItemDoesNotExist()