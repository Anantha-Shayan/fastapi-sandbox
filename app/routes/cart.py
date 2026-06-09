from fastapi import  APIRouter, HTTPException, status
from fastapi.params import Body
from app.schema import schema
from app.db import database
from app.services import cart_service, auth_service
from app.exceptions import exceptions

router = APIRouter(
    prefix="/cart"
)

@router.get('/')
def show_cart():
	cart = database.get_cart()
	if cart:
		return cart
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart Empty!")


@router.get('/{item_id}')
def get_item_from_cart(item_id: int):
	item = database.get_item_by_id(item_id)
	if item:
		return item
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

@router.post('/', status_code=status.HTTP_201_CREATED)
def add_item_to_cart(item : schema.AddToCart):
	try:
		return cart_service.add_item(item)
	except exceptions.ItemAlreadyExists:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Item already in cart!"
			)


@router.delete('/{item_name}', status_code=status.HTTP_204_NO_CONTENT)
def delete_item_from_cart(item_name: str):
	try:
		cart_service.delete_item(item_name)
	except exceptions.ItemDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def clear_cart_items():
	database.delete_cart()

@router.patch('/{item_id}', response_model=schema.ResUpdateQuantity)
def update_item_in_cart(item_id: int, item: schema.UpdateCart):
	try:
		return cart_service.update_item(item_id, item.quantity)
	except exceptions.ItemDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")