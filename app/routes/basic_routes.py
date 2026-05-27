from fastapi import APIRouter

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

@router.get('/items/{item_id}')
def get_items(item_id: int):
	return items_list.get(item_id)

@router.post('/items/{new}')
def add_item(new : str):
	return (f"Updated item list. Added {new}")