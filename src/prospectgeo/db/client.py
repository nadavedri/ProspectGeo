from psycopg2 import connect
import os
from prospectgeo.utils.logging_config import logger  
from prospectgeo.config import current_config


def _get_postgres_connection():
    logger.info("Attempting to establish a connection to the PostgreSQL database.")
    try:
        connection = connect(
            dbname=current_config.postgres_db,
            user=current_config.postgres_user,
            password=current_config.postgres_password,
            host=current_config.postgres_host,
            port=current_config.postgres_port,
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