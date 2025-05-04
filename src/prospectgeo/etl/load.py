from prospectgeo.db.client import get_db_client
from prospectgeo.db.queries import insert_qualification_results

from prospectgeo.config import current_config
from prospectgeo.utils.logging_config import logger


def batch_insert_data(qualification_results, db_type="postgres"):
    logger.info(
        "Starting batch_insert_data with %d results", len(qualification_results)
    )
    conn = get_db_client(db_type)
    cur = conn.cursor()
    query = insert_qualification_results()

    batch = []
    for result in qualification_results:
        batch.append(
            (
                result["user_id"],
                result["prospect_id"],
                result["qualifies"],
                result["qualification_timestamp"],
            )
        )

        if len(batch) >= current_config.write_chunk_size:
            logger.info("Inserting batch of size %d ", len(batch))
            cur.executemany(query, batch)
            batch = []

    if batch:
        logger.info("Inserting final batch of size %d", len(batch))
        cur.executemany(query, batch)

    conn.commit()
    logger.info("Batch insert completed successfully")
    cur.close()
    conn.close()
    logger.info("Database connection closed")
