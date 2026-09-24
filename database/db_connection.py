import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
load_dotenv()
from src.logger import get_logger

logger = get_logger("database")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}


def get_connection():

    try:
        connection = psycopg2.connect(**DB_CONFIG)

        logger.info("PostgreSQL connection established")

        return connection

    except Exception:
        logger.exception("Failed to connect to PostgreSQL")
        raise

def get_sqlalchemy_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=int(DB_CONFIG["port"]),
        database=DB_CONFIG["database"]
    )

    return create_engine(database_url)

    return engine

if __name__ == "__main__":
    try:
        connection = get_connection()

        print("PostgreSQL connection successful!")

        connection.close()

    except Exception as error:
        print("Database connection failed.")
        print(error)