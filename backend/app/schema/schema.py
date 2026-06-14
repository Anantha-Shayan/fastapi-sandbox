from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AddToCart(BaseModel):
    item_name : str
    quantity : int = Field(gt=0) # Quantity should be Greater Than 0

class UpdateCart(BaseModel):
    quantity : int = Field(gt=0)

class ResponseUpdateQuantity(BaseModel):
    message : str
    data : AddToCart

class LoginUser(BaseModel):
    email : EmailStr
    password : str = Field()

class CreateUser(LoginUser):
    user_name : str

class ResponseGetUserById(BaseModel):
    id : int
    user_name : str