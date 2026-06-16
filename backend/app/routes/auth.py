from fastapi import  APIRouter, HTTPException, status, Depends
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
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
	
	token = jwt.create_access_token(
		{
			"sub": str(user["id"])
		}
	)

	return {
		"access_token" : token,
		"token_type" : "bearer"
	}


# @router.get('/me')

	

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: schema.CreateUser):
	auth_service.create_new_user(user)
	return {
		"message" : "Registration successful!!!"
	}
