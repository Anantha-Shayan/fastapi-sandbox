import time
import logging
from fastapi import FastAPI, Request
from app.routes import cart
from app.db import database
from app.routes import auth, basic_routes
from app.exceptions import exceptions, handlers

app = FastAPI()

app.include_router(basic_routes.router)
app.include_router(auth.router)
app.include_router(cart.router)

@app.middleware("http")
async def process_time_header(request:Request, call_next):
	start = time.perf_counter()
	response = await call_next(request)
	end = time.perf_counter()
	response.headers["X-Process-Time"] = f"{str((end-start)*1000)}ms"
	return response
    

try:
    database.get_connection()
    print("Database connection successful")
except Exception as error:
    logging.info("Connecting to Database failed...")
    logging.error(error)


app.add_exception_handler(exceptions.UserAlreadyRegistered,handlers.user_already_exists)
app.add_exception_handler(exceptions.ItemAlreadyExists,handlers.item_already_exists)
app.add_exception_handler(exceptions.UserDoesNotExist, handlers.user_not_found)
app.add_exception_handler(exceptions.ItemDoesNotExist,handlers.item_not_found)
app.add_exception_handler(exceptions.InvalidCredential,handlers.invalid_credentials)