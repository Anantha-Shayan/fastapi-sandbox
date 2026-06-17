from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError
from app.services import auth_service
from app.utils import jwt
from app.exceptions import exceptions

# OAuth2PasswordBearer just extracts the Authorization: Bearer eyJ... (i.e.,access_token) from the incoming request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/user/auth/login')

def get_current_user(header: str = Depends(oauth2_scheme)):
    try:
        decoded = jwt.decode_access_token(header)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Unauthorized")
    try:
        user = auth_service.retrieve_user_by_id(decoded["sub"])
    except exceptions.UserDoesNotExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user