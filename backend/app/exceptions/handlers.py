from fastapi import status, Request
from fastapi.responses import JSONResponse


def user_already_exists(req: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "User already Registered"
        }
    )

def item_already_exists(req: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Item exists"
        }
    )

def item_not_found(req: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Item not found!"
        }
    )

def user_not_found(req: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "User not found!"
        }
    )

def invalid_credentials(req: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Invalid Credentials"
        }
    )