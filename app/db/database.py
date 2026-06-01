import psycopg
import os

DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")


def db_try():
        try:
            conn = psycopg.connect(dbname='first_db', host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD)
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")

            records = cur.fetchall()
            return records
        except Exception as e:
            print("Unable to connect to Database....")
            print("Error: ", e)