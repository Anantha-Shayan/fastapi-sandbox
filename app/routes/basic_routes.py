from fastapi import APIRouter, HTTPException, status
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
	if cart :
		return cart
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart is empty")

@router.get('/cart/{item_id}')
def get_cart_items(item_id: int):
	for i in cart:
		if i["id"] == item_id:
			return i
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	
def add_to_cart(item):
	for i in cart:
		if item.item_name.lower() == i["item_name"].lower():
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item already in cart")
	item_dict = item.dict()
	item_dict["id"] = max(i["id"] for i in cart) + 1
	cart.append(item_dict)

# Request body
@router.post('/cart', status_code=status.HTTP_201_CREATED) # Default will be 200 which is not ideal status 
#code when created something. Hence change the default to 201
def add_item_to_cart(item : AddToCart):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	add_to_cart(item)
	return {"message": "Item added to cart"}

def delete_item_from_cart(id):
	for i in cart:
		if i["id"] == id:
			cart.remove(i)
			return {"message" :"Item removed from cart"}
	raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart!")
	

@router.delete('/cart/{id}')
def delete_item(id : int):
	message = delete_item_from_cart(id)
	return message