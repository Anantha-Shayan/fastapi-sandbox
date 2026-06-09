from fastapi import  APIRouter, HTTPException, status
from fastapi.params import Body
from app.schema import schema
from app.db import database
from app.services import cart_service, auth_service
from app.exceptions import exceptions

router = APIRouter(
	prefix='/user'
)

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: schema.CreateUser):
	try :
		auth_service.create_new_user(user)
	except exceptions.UserAlreadyRegistered:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered!")
	return {
		"message" : "Registration successful!!!"
	}

@router.get('/{user_id}', response_model=schema.ResGetUserById)
def get_user_by_id(user_id: int):
	try :
		 user = auth_service.retrieve_user_by_id(user_id)
	except exceptions.UserDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User does not exist!")
	return user