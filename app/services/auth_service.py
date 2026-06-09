import psycopg
from app.schema import schema
from app.db import database
from app.exceptions import exceptions
from app.utils import utils


def create_new_user(user:schema.CreateUser):
    user.password = utils.hash_password(user.password)
    try:
        database.create_user(user)
    except psycopg.errors.UniqueViolation:
        raise exceptions.UserAlreadyRegistered()
    return {
        "message" : "Registration Sucessful!!!"
    }