from fastapi import FastAPI
from app.routes.basic_routes import router

app = FastAPI()

app.include_router(router)