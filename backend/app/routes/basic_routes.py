from fastapi import  APIRouter
from fastapi.params import Body

router = APIRouter()

@router.get('/')
def root():
	return {
		"message":"Welcome!"
	}