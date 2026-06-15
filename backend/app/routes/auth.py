from fastapi import  APIRouter, HTTPException, status, Depends
from fastapi.params import Body
from app.schema import schema
from app.db import database
from app.services import cart_service
from app.exceptions import exceptions
from app.utils import jwt
from app.services import auth_service
from fastapi.security.oauth2 import OAuth2PasswordBearer

# OAuth2PasswordBearer just extracts the Authorization: Bearer eyJ... (i.e.,access_token) from the incoming request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/auth/login')

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


@router.get('/me')
def get_user(header: str = Depends(oauth2_scheme)):
	decoded = jwt.decode_access_token(header)
	user = auth_service.retrieve_user_by_id(decoded["sub"])
	return user
	

@router.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(user: schema.CreateUser):
	try :
		auth_service.create_new_user(user)
	except exceptions.UserAlreadyRegistered:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered!")
	return {
		"message" : "Registration successful!!!"
	}
