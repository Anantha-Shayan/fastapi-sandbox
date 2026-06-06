from app.db.database import *
from app.schema.schema import *

class ItemAlreadyExists(Exception):
    pass

class ItemDoesNotExist(Exception):
    pass

def add_item(item):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	try:
		add_to_cart(item)
	except psycopg.errors.UniqueViolation:
		raise ItemAlreadyExists()
	return {"message": f"{item.item_name} added to cart"}

def update_item(item_id, quantity):
	updated_item = update_quantity(item_id, quantity)
	if not updated_item:
		raise ItemDoesNotExist()
	return {
		'message': "Item Quantity updated",
		'data' : updated_item
		}

def delete_item(item_name):
    deleted_item = delete_from_cart(item_name)
    if not deleted_item:
        raise ItemDoesNotExist()