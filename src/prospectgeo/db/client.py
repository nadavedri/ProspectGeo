from psycopg2 import connect
import os
from prospectgeo.utils.logging_config import logger  


def _get_postgres_connection():
    logger.info("Attempting to establish a connection to the PostgreSQL database.")
    try:
        connection = connect(
            dbname=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "password"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
        )
        logger.info("Successfully connected to the PostgreSQL database.")
        return connection
    except Exception as e:
        logger.error("Failed to connect to the PostgreSQL database: %s", e)
        raise


def get_db_client(db_type: str):
    logger.info("Requesting database client for DB type: %s", db_type)
    if db_type == "postgres":
        return _get_postgres_connection()
    logger.error("Unsupported DB type requested: %s", db_type)
    raise ValueError(f"Unsupported DB type: {db_type}")