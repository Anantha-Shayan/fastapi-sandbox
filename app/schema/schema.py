from pydantic import BaseModel, Field
from typing import Optional

class AddToCart(BaseModel):
    item_name : str
    quantity : int = Field(gt=0) # Quantity should be Greater Than 0

class UpdateCart(BaseModel):
    quantity : int = Field(gt=0)

class ResUpdateQuantity(BaseModel):
    message : str
    data : AddToCart