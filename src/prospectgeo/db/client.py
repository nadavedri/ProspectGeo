from psycopg2 import connect
import os


def _get_postgres_connection():
    return connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )


def get_db_client(db_type: str):
    if db_type == "postgres":
        return _get_postgres_connection()
    raise ValueError(f"Unsupported DB type: {db_type}")
