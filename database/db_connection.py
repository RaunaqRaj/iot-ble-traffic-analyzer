import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}


def get_connection():
    connection = psycopg2.connect(
        **DB_CONFIG
    )
    return connection


if __name__ == "__main__":
    try:
        connection = get_connection()

        print("PostgreSQL connection successful!")

        connection.close()

    except Exception as error:
        print("Database connection failed.")
        print(error)