from fastapi import FastAPI
from app.routes.basic_routes import router

app = FastAPI()

@app.get('/')
def root():
	return {
		"message":"/docs for Swagger"
	}

app.include_router(router)
