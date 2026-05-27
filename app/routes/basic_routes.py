from fastapi import APIRouter, HTTPException
from fastapi.params import Body
from app.schema.schema import AddToCart

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
	raise HTTPException(status_code=404, detail="Item not in cart!")
	
def add_to_cart(item):
	for i in cart:
		if item.item_name.lower() == i["item_name"].lower():
			raise HTTPException(status_code=409, detail="Item already in cart")
	item_dict = item.dict()
	item_dict["id"] = max(i["id"] for i in cart) + 1
	cart.append(item_dict)

# Request body
@router.post('/cart')
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	add_to_cart(item)
	return {"message": "Item added to cart"}