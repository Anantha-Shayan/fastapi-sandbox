from pwdlib import PasswordHash
from app.db.database import *
from app.schema.schema import *

class UserAlreadyRegistered(Exception):
    pass

password_hash = PasswordHash.recommended()

def hash_password(pwd):
    return password_hash.hash(pwd)

def create_new_user(user):
    user.password = hash_password(user.password)
    try:
        create_user(user)
    except psycopg.errors.UniqueViolation:
        raise UserAlreadyRegistered()
    return {
        "message" : "Registration Sucessful!!!"
    }