from fastapi import APIRouter
from fastapi.params import Body

router = APIRouter()

@router.get('/hello')
def hello():
	return {
		"message":"Hello!"
	}

items_list = {
	1: "Bat",
	2: "Ball"
}

@router.get('/items')
def items():
	return items_list.items()

@router.get('/items/{item_name}')
def get_items(item_name: str):
	for key, value in items_list.items():
		if item_name.lower() == value.lower():
			return key

# Request body
@router.post('/items')
def add_item(new : dict = Body(...)):	# Extracts all the fields from the Body -> Convert to python dict -> store in 'new'
	if new['name'] in items_list.values():
		return (f"Item {new['name']} exists")
	items_list[len(items_list) + 1] = new['name']
	return (f"Updated item list. Added {new['name']}")