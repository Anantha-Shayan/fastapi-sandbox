from fastapi import APIRouter
from fastapi.params import Body
from app.schema.schema import AddToCart
from random import randint

router = APIRouter()


@router.get('/')
def root():
	return {
		"message":"Welcome!"
	}


cart = [
	{
		"item_name" : "Earpods",
		"quantity" : 2,
		"id" : 1
	},
	{
		"item_name" : "Mobile",
		"quantity" : 1,
		"id" : 2
	}
]

@router.get('/cart')
def show_cart():
	return cart

@router.get('/cart/{item_id}')
def get_cart_items(item_id: int):
	for i in cart:
		if i["id"] == item_id:
			return i
	return "Item not in cart"
	
def add_to_cart(item):
	item_dict = item.dict()
	item_dict["id"] = randint(1,100000)
	cart.append(item_dict)

# Request body
@router.post('/cart')
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	for i in cart:
		if item.item_name.lower() == i["item_name"]:
			return "Item exists in cart"
	add_to_cart(item)
	return (f"{item.item_name} added to card")