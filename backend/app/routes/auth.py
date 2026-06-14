from fastapi import  APIRouter, HTTPException, status
from fastapi.params import Body
from app.schema import schema
from app.db import database
from app.services import cart_service
from app.exceptions import exceptions
from app.utils import jwt
from app.services import auth_service

router = APIRouter(
	prefix='/user',
	tags=['user']
)


@router.post('/auth/login')
def login_user(credentials: schema.LoginUser):
	try:
		user = auth_service.verify_user(credentials)
	except exceptions.InvalidCredential:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
	
	token = jwt.create_access_token(
		{
			"sub": str(user["id"])
		}
	)

	return {
		"access_token" : token,
		"token_type" : "bearer"
	}


@router.get('/auth/login/decode')
def get_jwt_decode(token_detail: dict):
	returned = jwt.decode_access_token(
		token_detail["access_token"]
	)
	return returned

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: schema.CreateUser):
	try :
		auth_service.create_new_user(user)
	except exceptions.UserAlreadyRegistered:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered!")
	return {
		"message" : "Registration successful!!!"
	}

@router.get('/{user_id}', response_model=schema.ResponseGetUserById)
def get_user_by_id(user_id: int):
	try :
		user = auth_service.retrieve_user_by_id(user_id)
	except exceptions.UserDoesNotExist:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User does not exist!")
	return user