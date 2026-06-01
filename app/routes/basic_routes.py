from fastapi import APIRouter, HTTPException, status
from fastapi.params import Body
from app.schema.schema import *
from app.db.database import *

router = APIRouter()


@router.get('/')
def root():
	return {
		"message":"Welcome!"
	}


@router.get('/cart')
def display_cart():
	return show_cart()

@router.get('/cart/{item_id}')
def get_cart_item(item_id: int):
	for i in cart:
		if i["id"] == item_id:
			return i
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

def add_to_cart(item):
	for i in cart:
		if item.item_name.lower() == i["item_name"].lower():
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already in cart")
	item_dict = item.dict()
	item_dict["id"] = max([i["id"] for i in cart], default=0) + 1 #default 0 for empty cart
	cart.append(item_dict)


# Request body
@router.post('/cart', status_code=status.HTTP_201_CREATED) # Default will be 200 which is not ideal status 
#code when created something. Hence change the default to 201
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	add_to_cart(item)
	return {"message": f"{item.item_name} added to cart"}


def delete_item_from_cart(item_id):
	for i in cart:
		if i["id"] == item_id:
			cart.remove(i)
			return {"message" :"Item removed from cart"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

@router.delete('/cart/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id : int):
	delete_item_from_cart(id)

@router.delete('/cart', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart():
	cart.clear()

@router.patch('/cart/{item_id}')
def update_quantity(item_id: int, item: UpdateCart):
	for i in cart:
		if i["id"] == item_id:
			i["quantity"] = item.quantity
			return {'message': "Item Quantity updated"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item id not in cart!")