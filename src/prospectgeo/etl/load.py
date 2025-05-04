from src.prospectgeo.db.client import get_db_client
from src.prospectgeo.db.queries import insert_qualification_query

from prospectgeo.config import current_config

def batch_insert_data(qualification_results, db_type="postgres"):
    conn = get_db_client(db_type)
    cur = conn.cursor()
    query = insert_qualification_query()
    
    batch = []
    for result in qualification_results:
        batch.append((result['user_id'], result['prospect_id'], result['qualifies']))
        
        if len(batch) >= current_config.write_chunk_size:
            cur.executemany(query, batch)
            batch = []
    
    if batch:
        cur.executemany(query, batch)
    
    conn.commit()
    cur.close()
    conn.close()
