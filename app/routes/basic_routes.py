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
def show_cart():
	cart = get_cart()
	# print(type(cart))
	if cart:
		return cart
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Empty!")


@router.get('/cart/{item_id}')
def get_item_from_cart(item_id: int):
	item = get_cart_item(item_id)
	if item:
		return item
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

# Request body
@router.post('/cart', status_code=status.HTTP_201_CREATED) # Default will be 200 which is not ideal status 
#code when created something. Hence change the default to 201
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	current_cart = get_cart()
	for i in current_cart:
		if i["item_name"] == item.item_name:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item exists in cart!")
	add_to_cart(item)
	return {"message": f"{item.item_name} added to cart"}


# def delete_item_from_cart(item_id):
# 	for i in cart:
# 		if i["id"] == item_id:
# 			cart.remove(i)
# 			return {"message" :"Item removed from cart"}
# 	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

@router.delete('/cart/{item_name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_name: str):
	current_cart = get_cart()
	for i in current_cart:
		if i["item_name"] == item_name:
			delete_from_cart(item_name)
			return {"message": "Item removed from cart"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")

@router.delete('/cart', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart_items():
	clear_cart()

@router.patch('/cart/{item_id}')
def update_quantity(item_id: int, item: UpdateCart):
	for i in cart:
		if i["id"] == item_id:
			i["quantity"] = item.quantity
			return {'message': "Item Quantity updated"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item id not in cart!")