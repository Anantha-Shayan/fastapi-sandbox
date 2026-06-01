from fastapi import FastAPI
from app.routes.basic_routes import router
from app.db.database import get_connection

app = FastAPI()

app.include_router(router)

try:
    get_connection()
    print("Database connection successful")
except Exception as error:
    print("Connecting to Database failed...")
    print(error)
