from fastapi import  APIRouter, HTTPException, status
from fastapi.params import Body
from app.schema.schema import *
from app.db.database import *
from app.services import cart_service, auth_service

router = APIRouter()

@router.get('/')
def root():
	return {
		"message":"Welcome!"
	}

@router.post('/user/register', status_code=status.HTTP_201_CREATED)
def register_user(user: CreateUser):
	try :
		auth_service.create_new_user(user)
	except auth_service.UserAlreadyRegistered:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered!")
	return {
		"message" : "Registration successful!!!"
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
	item = get_item_by_id(item_id)
	if item:
		return item
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

# Request body
@router.post('/cart', status_code=status.HTTP_201_CREATED) # Default will be 200 which is not ideal status 
#code when created something. Hence change the default to 201
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	try:
		return cart_service.add_item(item)
	except ItemAlreadyExists:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Item already in cart!"
			)

# def delete_item_from_cart(item_id):
# 	for i in cart:
# 		if i["id"] == item_id:
# 			cart.remove(i)
# 			return {"message" :"Item removed from cart"}
# 	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

@router.delete('/cart/{item_name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item_from_cart(item_name: str):
	try:
		delete_item(item_name)
	except ItemDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")


@router.delete('/cart', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart_items():
	clear_cart()

@router.patch('/cart/{item_id}', response_model=ResUpdateQuantity)
def update_item_in_cart(item_id: int, item: UpdateCart):
	try:
		return cart_service.update_item(item_id, item.quantity)
	except ItemDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")