from prospectgeo.db.client import get_db_client
from prospectgeo.db.queries import insert_qualification_results

from prospectgeo.config import current_config


def batch_insert_data(qualification_results, db_type="postgres"):
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
            cur.executemany(query, batch)
            batch = []

    if batch:
        cur.executemany(query, batch)

    conn.commit()
    cur.close()
    conn.close()
