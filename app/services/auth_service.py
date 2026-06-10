import psycopg
from app.schema import schema
from app.db import database
from app.exceptions import exceptions
from app.utils import security


def create_new_user(user:schema.CreateUser):
    user.password = utils.hash_password(user.password)
    try:
        database.create_user(user)
    except psycopg.errors.UniqueViolation:
        raise exceptions.UserAlreadyRegistered()
    return {
        "message" : "Registration Sucessful!!!"
    }

def verify_user(credentials):
    user = database.lookup_user(credentials.email)
    if not user:
	    raise exceptions.InvalidCredential()
    elif not security.verify_password(credentials.password, user["password"]):
        raise exceptions.InvalidCredential()
    
def retrieve_user_by_id(user_id: int):
    user = database.get_user(user_id)
    if user:
        return user
    else:
        raise exceptions.UserDoesNotExist()