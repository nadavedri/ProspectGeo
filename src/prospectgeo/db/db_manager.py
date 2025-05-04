from .client import get_db_client
from .schemas.postgres.qualification_results_schema import (
    create_qualification_results_schema,
)
from prospectgeo.utils.logging_config import logger  


def create_all_schemas():
    logger.info("Starting schema creation process.")
    try:
        postgres_conn = get_db_client("postgres")
        logger.info("Successfully obtained PostgreSQL connection.")
        create_qualification_results_schema(postgres_conn)
        logger.info("Successfully created qualification results schema.")
    except Exception as e:
        logger.error("An error occurred during schema creation: %s", e)
        raise
    finally:
        if 'postgres_conn' in locals() and postgres_conn:
            postgres_conn.close()
            logger.info("PostgreSQL connection closed.")