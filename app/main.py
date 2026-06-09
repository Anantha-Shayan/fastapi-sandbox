import time
from fastapi import FastAPI, Request
from app.routes import basic_routes
from app.db import database

app = FastAPI()

app.include_router(basic_routes.router)

@app.middleware("http")
async def process_time_header(request:Request, call_next):
	# print("Middleware called")
	start = time.perf_counter()
	response = await call_next(request)
	end = time.perf_counter()
	response.headers["X-Process-Time"] = f"{str((end-start)*1000)}ms"
	return response
    

try:
    database.get_connection()
    print("Database connection successful")
except Exception as error:
    print("Connecting to Database failed...")
    print(error)
