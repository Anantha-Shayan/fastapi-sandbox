FROM python:3.10-slim 
#psycopg,argon2,etc., are not compatible with alpine

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]