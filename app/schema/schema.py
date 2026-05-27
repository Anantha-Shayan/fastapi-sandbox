from pydantic import BaseModel

class AddToCart(BaseModel):
    item_name : str
    quantity : int
