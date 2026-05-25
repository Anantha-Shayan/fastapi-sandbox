from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def print_hello():
	return("Hello World")
