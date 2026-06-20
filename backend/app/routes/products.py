from fastapi import  APIRouter, HTTPException, status, Query
from fastapi import Depends
from app.schema import schema
from app.db import database
from app.services import prod_service
from app.exceptions import exceptions
from app.services import auth_service
from app.dependencies import auth_dep


router = APIRouter(
    prefix = '/products',
    tags = ['products']
)

@router.get('/')
def show_products(limit: int = Query(10, ge=1, le=100)):
    prod_service.show_prod(limit)