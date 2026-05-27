from fastapi import APIRouter
from fastapi.params import Body
from app.schema.schema import AddToCart


router = APIRouter()


@router.get('/')
def root():
	return {
		"message":"Welcome!"
	}


cart = {
	1 :	{
			"item_name" : "Earpods",
			"quantity" : 2
		},
	2 :	{
			"item_name" : "Mobile",
			"quantity" : 1
		}
}

@router.get('/cart')
def show_cart():
	return cart.items()

@router.get('/cart/{item_id}')
def get_cart_items(item_id: int):
	return cart.get(item_id)

# Request body
@router.post('/cart')
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	if item.item_name.lower() in cart.items():
		return "Item exists in cart"
	item_name = item.item_name
	item = item.dict()
	cart[len(cart)+1] = item
	return (f"{item_name} added to cart!")