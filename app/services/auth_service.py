from app.db.database import *
from app.schema.schema import *

class UserAlreadyRegistered(Exception):
    pass

def create_new_user(user):
    try:
        create_user(user)
    except psycopg.errors.UniqueViolation:
        raise UserAlreadyRegistered()
    return {
        "message" : "Registration Sucessful!!!"
    }